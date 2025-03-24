from typing import Any

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.db_config import async_session_maker
from db.models.users.repository import UsersRepository
from telegram.commands import set_main_menu
from telegram.keyboards.inline.inline import to_signup, to_car_register

from loguru import logger

from telegram.states.signup_users import SignupUserStates

router = Router(name="LETS FKING START")


@router.message(CommandStart())
async def start(message: Message, user: Any):
    try:
        await message.bot.delete_my_commands()
        await message.delete()

        if user:
            await message.answer("Вы уже зарегистрированы!")
            await set_main_menu(message.bot)

        await message.answer(
            text="Добро пожаловать в нашу команду <b>GearMind</b> 😇\n"
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


@router.callback_query(F.data == "signup")
async def signup(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id
        )
        get_name_message = await callback.message.answer(
            "Итак, регистрация простая, требуется "
            "всего-лишь <b>Ваше имя</b>\n"
            "\n"
            "Напишите, пожалуйста, его ниже 👇"
        )
        await state.set_state(SignupUserStates.name)
        await state.set_data({"message_id": get_name_message.message_id})
    except Exception as e:
        logger.error(f"signup: {e}")
        await callback.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


@router.message(SignupUserStates.name)
async def get_name(message: Message, state: FSMContext):
    try:
        message_id = await state.get_value("message_id")

        await message.bot.delete_message(message.chat.id, message_id)
        await message.delete()

        async with async_session_maker() as session:
            new_user = await UsersRepository.add(
                session=session,
                tg_user_id=message.from_user.id,
                name=message.text
            )

        if not new_user:
            await message.answer(
                "❌ Произошла ошибка при регистрации, пожалуйста, попробуйте снова!"
            )
            return False

        await message.answer(
            text=f"✅ Отлично, {new_user.name}! Теперь мы можем начинать работу\n"
                 "\n"
                 "Итак, для того, чтобы <b>полноценно использовать нашу систему</b> Вам потребуется "
                 "предоставить информацию о своей машине. Это можно сделать по кнопке ниже 👇",
            reply_markup=to_car_register
        )
        await set_main_menu(message.bot)
    except Exception as e:
        logger.error(f"Get User Name: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()
