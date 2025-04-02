from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import UsersRepository

from config import settings
from logger import logger


class UserDataMiddleware(BaseMiddleware):
    def __init__(self, repository: UsersRepository):
        super().__init__()
        self.repository = repository

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        """Мидлварь для проверки пользователя на наличие в системе"""
        user_id = None
        user = None
        session: AsyncSession = data.get("session")

        try:
            if event.message:
                user_id = event.message.from_user.id

            elif event.callback_query:
                user_id = event.callback_query.from_user.id

            if user_id is not None:
                user = await self.repository.find_one_or_none(session, tg_user_id=user_id)

                if user and user.tg_user_id == settings.BOT_ID:
                    return await handler(event, data)

                if not user:
                    logger.critical(f"Не нашли юзера с tg_id: {user_id}")

            data["user"] = user

            return await handler(event, data)
        except Exception as e:
            logger.critical(f"Ошибка в UserDataMiddleware: {e}")
            return None