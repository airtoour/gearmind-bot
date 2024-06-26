from aiogram.types import Message

from src.telegram.keyboards.inline.inline import to_signup
from src.db.models.models import Users
from src.telegram.bot import logger


async def start(message: Message):
    try:
        user = Users.get_user_by_tg(message.from_user.id)

        signup_user = to_signup()

        if user:
            await message.answer(
                "Привет! Рады, что ты вернулся к нам!\n"
                "Давай посмотрим меню!"
            )
        else:
            await message.answer(
                "Добро пожаловать в нашу команду AUTOCOMP!\n"
                "Я умею искать товары на различных маркетплейсах товары, которые требуются тебе.\n"
                "Все интересующие тебя вопросы ты сможешь узнать сразу после регистрации!"
                "\n"
                "Давай зарегистрируем тебя по кнопке ниже", reply_markup=signup_user
            )
    except Exception as e:
        logger.exception("start:", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы...."
        )
