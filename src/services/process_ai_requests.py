import uuid
from datetime import datetime
from typing import Dict, Union

from pydantic import ValidationError

from ai import yandex, CompletionCreateSchema

from sqlalchemy.ext.asyncio import AsyncSession
from db.models import (
    Requests,
    Prompts,
    Cars,
    Users,
    CarsRepository,
    PromptsRepository,
    RequestsRepository
)
from telegram.utils.utils import get_formatted_prompt

from logger import logger


class RequestAIService:
    """Сервис работы ИИ в системе"""
    def __init__(
        self,
        ai: yandex,
        request: str,
        prompt_type: str,
        user: Users,
        session: AsyncSession
    ):
        self.ai = ai
        self.request = request
        self.prompt_type = prompt_type
        self.user = user
        self.session = session

    async def create(self) -> Union[str, None]:
        """Полный процесс работы с запросом ИИ"""
        try:
            # Пытаемся получить промпт
            prompt = await self._get_prompt(self.session)

            # Пытаемся получить автомобиль пользователя
            car = await self._get_car(self.session)

            # Если нет промпта, выдаём ошибку
            if not prompt:
                raise RuntimeError("Нет подходящего промпта...")

            # Если нет автомобиля, выдаём ошибку
            if not car:
                raise RuntimeError("Нет автомобиля для работы с пользователем...")

            # Валидируем данные для запроса к ИИ
            try:
                request_data = CompletionCreateSchema(
                    prompt=get_formatted_prompt(prompt.text, self.user.name, car.full),
                    text=self.request
                )
            except ValidationError as e:
                logger.error(e)
                return

            # Отравляем запрос к ИИ
            result = await self.ai.create(request_data)

            # Если результат вернулся с ошибкой
            if not result:
                raise RuntimeError("Нет ответа от YandexGPT...")

            # Отправляем ответ запроса в БД
            added_request = await self._add_to_requests(
                session=self.session,
                prompt_id=prompt.id,
                response_text=result.text,
                usage=result.usage.model_dump(mode="json")
            )

            # Если запись не появилась в БД
            if not added_request:
                raise RuntimeError("Не получилось логировать информацию об использовании запроса...")

            return result.text, added_request.id
        except Exception as e:
            logger.error(e)
            return None

    async def _add_to_requests(
        self,
        session: AsyncSession,
        prompt_id: uuid.UUID,
        response_text: str,
        usage: Dict[str, str]
    ) -> Requests:
        """Отправка в Базу данных информацию об использовании ИИ в контексте запроса"""
        return await RequestsRepository.add(
            session=session,
            date=datetime.now(),
            prompt_id=prompt_id,
            text=self.request,
            response=response_text,
            response_data=usage,
        )

    async def _get_prompt(self, session: AsyncSession) -> Prompts:
        """Получение промпта по запросу"""
        return await PromptsRepository.find_one_or_none(
            session, type=self.prompt_type
        )

    async def _get_car(self, session: AsyncSession) -> Cars:
        """Получение автомобиля пользователя"""
        return await CarsRepository.find_one_or_none(
            session, user_id=self.user.id
        )
