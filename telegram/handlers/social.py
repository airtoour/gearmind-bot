from aiogram.types import Message
from src.telegram.keyboards.inline.inline import social_links
from src.telegram.bot import logger


async def social(message: Message):
    try:
        markup = social_links()
        await message.answer(
            'Хочешь узнать лучше о нас?\n'
            'Переходи по ссылкам на социальные сети ниже!', reply_markup=markup
        )
    except Exception as e:
        logger.exception("social", e)
