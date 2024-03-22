from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F

from bot import bot, dp
from src.db.config import session
from src.telegram.states import UserStates
from src.models import Users
from src.exceptions import server_exceptions
from src.telegram.keyboards.inline.inline import signup_tap_link


@dp.message_handler(Command('start'))
async def start(message: Message, state: FSMContext):
    user = session.query(Users).filter_by(tg_user_id=message.from_user.id).first()

    if user:
        await message.answer('Привет, рад, что ты вернулся, что-то снова случилось с твоей машиной?\n'
                             'Давай будем думать, что тебе поможет, опиши свою проблему!')
    else:
        markup = signup_tap_link(message.from_user.id)
        await message.answer('Привет, тебя приветствует команда "AUTOCOMP"\n'
                             'Если ты к нам обратился, значит с твоей машиной что-то не так :(\n'
                             'Это грустно. Поэтому давай сначала познакомимся,'
                             'а потом будем подбирать тебе компоненты.', reply_markup=markup)
        await state.set_state(UserStates.registration)
