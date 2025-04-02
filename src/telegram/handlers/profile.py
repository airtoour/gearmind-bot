from typing import Any

from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message

from logger import logger


router = Router(name="Work With User`s Profile")


@router.message(Command("profile"))
async def profile(message: Message, user: Any):
    try:
        await message.answer(
            "Пожалуйста, <b>Ваш профиль</b> 👇\n\n"
            f"▪️ <b>Имя</b>: {user.name}"
        )
    except (Exception, TelegramAPIError) as e:
        logger.error(f"Profile Content: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
