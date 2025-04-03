from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from db.db_config import get_session_bot


class DbSessionMiddleware(BaseMiddleware):
    """Мидлварь для создания сессий в хендлерах"""
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with get_session_bot() as session:
            data["session"] = session
            return await handler(event, data)
