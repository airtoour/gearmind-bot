import asyncio

from aiogram.exceptions import TelegramAPIError
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from db.models.users.repository import UsersRepository
from telegram.keyboards.inline.inline import to_car_register, first_param

from logger import logger


TABLES_TEXT_MAPPING: dict[str, str] = {
    "Масла":
        "Выберите, пожалуйста вид масла, который Вы чаще "
        "всего используете для своей машины, "
        "чтобы подобрать новое ниже",
    "Шины":
        "Выберите, пожалуйста, диаметр Ваших шин, "
        "чтобы подобрать новые ниже",
    "Аккумуляторы":
        "Выберите, пожалуйста, ёмкость аккумулятора, "
        "который, приемлем для Вашей машины, чтобы "
        "подобрать подходящий ниже",
    "Диски":
        "Выберите, пожалуйста, диаметр твоих дисков, "
        "чтобы подобрать новые ниже",
}


async def process_user(message: Message, state: FSMContext, phone: str):
    """Обработка регистрации пользователя через номер телефона"""
    try:
        await state.update_data(phone=phone)

        approved_phone = await message.answer(
            text=f"✅ Номер телефона принят!",
            reply_markup=ReplyKeyboardRemove()
        )
        await UsersRepository.add(
            tg_user_id=message.from_user.id,
            tg_username=message.from_user.username,
            first_name=message.from_user.first_name,
            phone_number=await state.get_value("phone")
        )
        await asyncio.sleep(1)
        await message.bot.delete_message(
            chat_id=message.from_user.id,
            message_id=approved_phone.message_id
        )
        await message.answer(
            text="✅ Отлично! Теперь мы можем начинать работу\n"
                 "\n"
                 "Итак, для того, чтобы <b>полноценно использовать нашу систему</b> Вам потребуется "
                 "предоставить информацию о своей машине. Это можно сделать по кнопке ниже 👇",
            reply_markup=to_car_register
        )
        return True
    except Exception as e:
        logger.error(f"process_user: {e}")
        return False
    finally:
        await state.clear()


async def get_problem_field(callback: CallbackQuery, table: str):
    try:
        text = TABLES_TEXT_MAPPING.get(table, "")

        await callback.message.answer(text=text, reply_markup=first_param(table))

        return True
    except (Exception, TelegramAPIError) as e:
        logger.error(e)
        return False
