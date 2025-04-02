from typing import Dict, Union

from httpx import AsyncClient, HTTPError
from pydantic import ValidationError

from ai.yandex.schemas import (
    CompletionCreateSchema,
    UsageCreateSchema,
    ReturnCreateSchema
)

from logger import logger
from config import settings


class YandexGPTClient:
    def __init__(
        self,
        token: str,
        model: str,
        catalog_id: str
    ):
        self.token = token
        self.model = model
        self.catalog_id = catalog_id

        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.token}"
        }

        self.client = AsyncClient(headers=self.headers)

    async def create(self, data: CompletionCreateSchema) -> Union[ReturnCreateSchema, None]:
        """Запрос в сторону YandexGPT для получения ответа от ИИ"""
        try:
            # Формирование json для отправки запроса
            payload = {
                "modelUri": f"gpt://{self.catalog_id}/{self.model}/rc",
                "completionOptions": {
                    "stream": False,
                    "temperature": data.temperature,
                    "maxTokens": data.max_tokens
                },
                "messages": [
                    {
                        "role": "system",
                        "text": data.prompt
                    },
                    {
                        "role": "user",
                        "text": data.text
                    }
                ]
            }

            # Отправка запроса
            response = await self.client.post(url=data.url, json=payload, timeout=30)
            response.raise_for_status()

            # Получение ответа в виде json
            result = response.json()

            # Валидация схемы использования токенов
            try:
                usage_data = UsageCreateSchema(
                    input_tokens=result["result"]["usage"]["inputTextTokens"],
                    completion_tokens=result["result"]["usage"]["completionTokens"],
                    total_tokens=result["result"]["usage"]["totalTokens"]
                )
            except ValidationError as e:
                logger.error(e)
                return None

            # Валидация ответа от ИИ
            try:
                result_data = ReturnCreateSchema(
                    text=result["result"]["alternatives"][0]["message"]["text"],
                    usage=usage_data
                )
            except ValidationError as e:
                logger.error(e)
                return None

            return result_data
        except HTTPError as e:
            logger.error(e)
            return None


# Определяем клиент YandexGPT
yandex = YandexGPTClient(
    token=settings.YANDEX_TOKEN,
    model=settings.YANDEX_MODEL,
    catalog_id=settings.YANDEX_CATALOG
)
