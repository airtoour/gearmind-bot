from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.telegram.bot import logger, bot
from src.db.models.models import Users

async def solution(message: Message, state: FSMContext):
    try:
        user = Users.get_user_by_tg(message.from_user.id)
        if user:
            await message.answer(
                "Наконец-то мы добрались до самого вкусного! Прости, я это так.. Кхм...\n"
                "Итак, опиши свою проблему ниже, а я постараюсь помочь тебе в этом.\n"
                "\n"
                ""
            )
