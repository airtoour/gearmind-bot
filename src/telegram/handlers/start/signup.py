from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram.bot import bot
from telegram.filters.menu import set_main_menu
from telegram.keyboards.reply.reply import get_phone
from telegram.states.signup_users import SignupUserStates
from telegram.utils.utils import process_user

from loguru import logger


router = Router(name="signup")


@router.callback_query(F.data == "signup")
async def signup(callback: CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id
        )

        await callback.message.answer(
            text="Итак, регистрация простая, требуется "
                 "всего-лишь Ваш номер телефона.\n"
                 "\n"
                 "<blockquote>"
                 "<b>НОМЕР ТЕЛЕФОНА ТРЕБУЕТСЯ ДЛЯ ТОГО, ЧТОБЫ ПОЛУЧАТЬ "
                 "ПОЛЕЗНЫЕ УВЕДОМЛЕНИЯ В БУДУЩЕМ!</b>\n"
                 "</blockquote>",
            reply_markup=get_phone
        )
        await state.set_state(SignupUserStates.phone)
    except Exception as e:
        logger.error(f"signup: {e}")
        await callback.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


@router.message(SignupUserStates.phone, F.contact)
async def get_contact(message: Message, state: FSMContext):
    try:
        if message.contact.user_id != message.from_user.id:
            await message.answer("Отправьте, пожалуйста, корректный номер телефона")
            return

        await process_user(message, state, message.contact.phone_number)
        await set_main_menu(bot)
    except Exception as e:
        logger.exception("get_phone", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()
