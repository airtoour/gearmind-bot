from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.exceptions import TelegramAPIError, AiogramError

from src.telegram.bot import dp
from src.db.config import session
from src.telegram.states import UserStates
from src.models import Users
from src.exceptions import server_exceptions
from src.telegram.keyboards.inline.inline import signup_tap_link


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    try:
        user = session.query(Users).filter_by(tg_user_id=message.from_user.id).first()

        if user:
            await message.answer('Привет, рад, что ты вернулся, что-то снова случилось с твоей машиной?\n'
                                 'Давай будем думать, что тебе поможет, опиши свою проблему!')
        else:
            markup = signup_tap_link()
            await message.answer('Привет, тебя приветствует команда "AUTOCOMP"\n'
                                 'Если ты к нам обратился, значит с твоей машиной что-то не так :(\n'
                                 'Это грустно. Поэтому давай сначала познакомимся\n'
                                 'а потом будем подбирать тебе компоненты.', reply_markup=markup)

            await message.answer('Если ты успешно прошел(ла) регистрацию в форме, то напиши, пожалуйста,'
                                 'свой номер телефона, чтобы я проверил информацию')
            await state.set_state(UserStates.confirm_signup)
    except TelegramAPIError or AiogramError as e:
        print(server_exceptions(status_code=422,
                          detail=f'Ошибка во время работы бота: {e}'))


@dp.message(UserStates.confirm_signup)
async def confirm_signup(message: Message, state: FSMContext):
    try:
        while True:
            phone_number = str(message.text)

            registered_phone = session.query(Users).filter_by(phone_number=phone_number).first()

            if registered_phone.phone_number:
                if (registered_phone.tg_username is None
                        and registered_phone.tg_user_id is None
                        and registered_phone.phone_number == phone_number):
                    await Users.tg_insert(tg_user_id=message.from_user.id,
                                          tg_username=message.from_user.username,
                                          phone_number=phone_number)
                    await message.answer('Регистрация успешно подтверждена! Добро пожаловать в нашу команду\n'
                                         'Давай узнаем что случилось с твоей машиной и посмотрим Меню. КНОПКИ МЕНЮ')
                else:
                    await message.answer('Регистрация уже подтверждена! КНОПКИ МЕНЮ')
                break
            else:
                await message.answer('Такого номера не существует! Попробуй снова!')
    except Exception as e:
        print('ПОДТВЕРЖДЕНИЕ РЕГИСТРАЦИИ: ', e)
