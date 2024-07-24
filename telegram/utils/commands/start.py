from aiogram.types import Message

from telegram.keyboards.inline.inline import to_signup
from db.users.dao import UsersDAO

from logger import logger


async def start(message: Message):
    try:
        user = await UsersDAO.get_by_tg(message.from_user.id)
        print(user)

        if user:
            await message.answer(
                "Привет! Рады, что Вы вернулись к нам!\n"
                "Давайте посмотрим меню!"
            )
        else:
            await message.answer(
                "Добро пожаловать в нашу команду <b>AUTOCOMP</b>!\n"
                "Я умею искать товары на различных маркетплейсах товары, которые требуются Вам.\n"
                "Все интересующие Вас вопросы Вы сможете узнать сразу после регистрации!"
                "\n"
                "Давайте зарегистрируем Вас по кнопке ниже", reply_markup=to_signup()
            )
    except Exception as e:
        logger.error(e, exc_info=True)
        await message.answer(
            "Кажется, произошла какая-то ошибка, извините, пожалуйста, мы решаем эти проблемы...."
        )
