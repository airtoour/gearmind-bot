from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from telegram.keyboards.inline.inline import to_signup

from loguru import logger


router = Router(name="start")


@router.message(CommandStart())
async def start(message: Message):
    try:
        await message.bot.delete_my_commands()
        await message.delete()

        await message.answer(
            text="Добро пожаловать в нашу команду <b>AUTOCOMP</b> 😇\n"
                 "\n"
                 "▫️ Я умею искать товары на различных маркетплейсах, которые мы сможем Вам подобрать\n"
                 "▫️ Все интересующие Вас вопросы ты сможешь узнать сразу после регистрации!"
                 "\n"
                 "Давайте зарегистрируем Вас по кнопке ниже 👇",
            reply_markup=to_signup
        )
    except Exception as e:
        logger.exception(f"start: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка, извините, "
            "пожалуйста, мы решаем эти проблемы...."
        )
