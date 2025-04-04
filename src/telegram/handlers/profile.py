from typing import Any

from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message

from telegram.keyboards.inline.inline import profile_keyboard

from logger import logger


router = Router(name="Work With User`s Profile")


@router.message(Command("profile"))
async def profile(message: Message, user: Any):
    try:
        await message.answer(
            text="Пожалуйста, <b>Ваш профиль</b> 👇\n\n"
                 f"▪️ <b>Имя</b>: {user.name}",
            reply_markup=profile_keyboard(user.role)
        )
    except (Exception, TelegramAPIError) as e:
        logger.error(f"Profile Content: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
