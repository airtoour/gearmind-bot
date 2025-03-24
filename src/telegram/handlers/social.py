from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from telegram.keyboards.inline.inline import social_links

from loguru import logger


router = Router(name="Social Links")


@router.message(Command("social"))
async def social(message: Message):
    try:
        await message.delete()

        await message.answer(
            text="Хотите узнать лучше о нас?\n"
                 "Переходите по ссылкам на социальные сети ниже!\n"
                 "\n"
                 "Подписавшись, Вы сможете получать самую актуальную "
                 "информацию и следить за обновлениями нашего сервиса 🫶\n"
                 "\n\n"
                 "<blockquote>"
                 "<i>* - Признана экстремистской соц. сетью на территории РФ</i>"
                 "</blockquote>",
            reply_markup=social_links
        )
    except Exception as e:
        logger.exception("social", e)
