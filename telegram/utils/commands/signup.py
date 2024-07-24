from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram.bot import bot
from telegram.states import UserStates
from telegram.keyboards.inline.inline import to_car_register
from db.users.sync_repository import SyncUsersRepository

from logger import logger


async def signup(callback_query: CallbackQuery, state: FSMContext):
    try:
        user = SyncUsersRepository.get_by_tg(callback_query.from_user.id)

        if user:
            await bot.send_message(
                callback_query.from_user.id,
                f"{callback_query.from_user.first_name}, ты зарегистрирован у нас!\n"
                f"Тебе доступны мои инструменты, взгляни на меню."
            )
        else:
            await bot.send_message(
                callback_query.from_user.id,
                "Итак, регистрация простая, требуется всего-лишь Ваш номер телефона.\n"
                "Напишите его, пожалуйста, и мы сможем продолжать работу."
                "\n"
                "```\n"
                "НОМЕР ТЕЛЕФОНА ТРЕБУЕТСЯ ДЛЯ ТОГО, ЧТОБЫ ПОЛУЧАТЬ ПОЛЕЗНЫЕ УВЕДОМЛЕНИЯ В БУДУЩЕМ!\n"
                "```\n"
            )
            await state.set_state(UserStates.phone)
    except Exception as e:
        logger.exception("signup", e)
        await bot.send_message(
            callback_query.from_user.id,
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


async def get_phone(message: Message, state: FSMContext):
    try:
        await state.update_data(phone=message.text)
        get_data = await state.get_data()

        tg_id = message.from_user.id
        tg_username = message.from_user.username
        first_name = message.from_user.first_name
        phone = get_data.get('phone')

        await UsersDAO.add(
            tg_user_id=tg_id,
            tg_username=tg_username,
            first_name=first_name,
            phone_number=phone
        )

        await message.answer(
            f"Отлично, {first_name}! Теперь мы можем начинать работу.\n"
            "Итак, для того, чтобы полноценно использовать нашу систему Вам потребуется "
            "предоставить информацию о своей машине. Это можно сделать по кнопке ниже",
            reply_markup=to_car_register()
        )
    except Exception as e:
        logger.exception("get_phone", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()
