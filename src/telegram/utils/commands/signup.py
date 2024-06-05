from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from src.telegram.bot import bot
from src.telegram.states import UserStates
from src.telegram.keyboards.inline.inline import to_car_register
from src.db.models.models import Users


async def signup(callback_query: CallbackQuery, state: FSMContext):
    try:
        user = Users.get_user_by_tg(callback_query.from_user.id)

        if user:
            await bot.send_message(
                callback_query.from_user.id,
                f"{callback_query.from_user.first_name}, ты зарегистрирован у нас!\n"
                f"Тебе доступны мои инструменты, взгляни на меню."
            )
        else:
            await bot.send_message(
                callback_query.from_user.id,
                "Итак, регистрация простая, требуется всего-лишь твой номер телефона.\n"
                "Напиши его, и мы сможем продолжать работу."
            )
            await state.set_state(UserStates.phone)
    except Exception as e:
        print("start: ", e)
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

        new_user = Users.create(tg_id, tg_username, first_name, phone)

        await message.answer(
            f"Отлично, {first_name}! Теперь мы можем начинать работу.\n"
            "Итак, для того, чтобы полноценно использовать нашу систему тебе потребуется "
            "предоставить информацию о своей машине. Это можно сделать по кнопке ниже", reply_markup=to_car_register()
        )
    except Exception as e:
        print("get_phone start: ", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()