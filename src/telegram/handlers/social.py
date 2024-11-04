from aiogram.types import Message
from src.telegram.keyboards.inline.inline import social_links

from loguru import logger


async def social(message: Message):
    try:
        await message.answer(
            text="Хочешь узнать лучше о нас?\n"
                 "Переходи по ссылкам на социальные сети ниже!",
            reply_markup=social_links
        )
    except Exception as e:
        logger.exception("social", e)
