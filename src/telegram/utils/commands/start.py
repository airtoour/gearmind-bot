from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.models.users import Users
from src.telegram.states import UserStates
# from src.db.db import app


async def start(message: Message, state: FSMContext):
    try:
        user = Users.get_current(message.from_user.id)

        if user:
            await message.answer(
                'Привет, рад, что ты вернулся, что-то снова случилось с твоей машиной?\n'
                'Давай будем думать, что тебе поможет, опиши свою проблему!'
            )
        else:
            await message.answer(
                'Привет, тебя приветствует команда "AUTOCOMP"\n'
                'Если ты к нам обратился, значит с твоей машиной что-то не так\n'
                'Это грустно. Поэтому давай сначала познакомимся\n'
                'а потом будем подбирать тебе компоненты.\n'
                '\n'
                'Напиши свой номер телефона. Формат номера телефона - +79876543210'
            )
            await state.set_state(UserStates.user_phone)
    except Exception as e:
        await message.answer(
            'Кажется, произошла какая-то ошибка.\n'
            'Стараемся разобраться с этим, извините за неудобства...'
        )
        print('start:', e)


async def phone(message: Message, state: FSMContext):
    try:
        await state.update_data(phone=message.text)

        await message.answer(
            "Отлично! А теперь свой город. Это нужно для того, "
            "чтобы я смог подбирать товары исходя из твоего города проживания"
        )
        await state.set_state(UserStates.user_city)
    except Exception as e:
        await message.answer(
            'Кажется, произошла какая-то ошибка.\n'
            'Стараемся разобраться с этим, извините за неудобства...'
        )
        print('phone:', e)

async def city(message: Message, state: FSMContext):
    try:
        with app.app_context():
            await state.update_data(city=message.text)
            get_data = await state.get_data()
            user_phone = get_data.get('phone')
            user_city = get_data.get('city')

            print(user_phone, user_city)

            new_user = Users.create(
                tg_user_id=message.from_user.id,
                tg_username=message.from_user.username,
                first_name=message.from_user.first_name,
                phone_number=user_phone,
                city_name=user_city
            )
            print(new_user)
            await message.answer(
                "Круто! Теперь у меня есть все, для того, чтобы я смог впредь помогать тебе.\n"
                "Теперь, можем начать работать. Ты можешь начать с кнопки меню слева от поля ввода."
            )
    except Exception as e:
        await message.answer(
            'Кажется, произошла какая-то ошибка.\n'
            'Стараемся разобраться с этим, извините за неудобства...'
        )
        print('city:', e)
    finally:
        await state.clear()