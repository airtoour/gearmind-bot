from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.telegram.states import UserStates
from src.telegram.keyboards.inline.inline import signup_tap_link

from src.db.repository.users import get_user_by_tg, get_user
from src.db.db import session

async def start(message: Message, state: FSMContext):
    markup = signup_tap_link()

    try:
        user = get_user_by_tg(message.from_user.id)

        if user:
            await message.answer(
                f"Привет, {message.from_user.first_name}!\n"
                f"Снова что-то случилось? Давай решать! Глянем на меню!"
            )
        else:
            await message.answer(
                "Добро пожаловать!\n"
                "Для того, чтобы начать со мной работу требуется регистрация.\n"
                "Давай перейдём по ссылке ниже, там тебя ждёт форма регистрации.", reply_markup=markup
            )
            await message.answer(
                "Как только ты пройдёшь регистрацию, напиши сюда номер телефона, который ты указал в форме.\n"
                "Это подтвердит твою регистрацию в нашей системе и позволит продолжить работу!"
            )
            await state.set_state(UserStates.user_phone)
    except Exception as e:
        print("start: ", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


async def get_phone(message: Message, state: FSMContext):
    try:
        await state.update_data(phone=message.text)
        get_data = await state.get_data()
        phone = get_data.get('phone')

        user = get_user(phone)

        if user.tg_user_id is None and user.tg_username is None:
            user.tg_user_id = message.from_user.id
            user.tg_username = message.from_user.username
            session.commit()

            await message.answer(
                "Отлично! Регистрация подтверждена! Теперь мы можем начинать работу.\n"
                "Итак, нажимай на команду /problem и действуй по инструкции, удачи тебе, друг!"
            )
        else:
            await message.answer("Кажется, ты уже есть у нас в ")
    except Exception as e:
        print("get_phone start: ", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()