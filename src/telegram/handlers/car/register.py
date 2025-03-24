from typing import Union, Any

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from db.db_config import async_session_maker
from db.models.cars.repository import CarsRepository

from telegram.states.signup_car import SignupUserCarStates
from telegram.states.update_car_info import UpdateCarInfo
from telegram.keyboards.reply.reply import car_info_confirm
from telegram.keyboards.inline.inline import car_list, lets_solution, retry_register_car

from logger import logger


router = Router(name="Work with User`s Car")


@router.message(Command("car"))
@router.callback_query(F.data.in_(["car", "retry_register_car"]))
async def car(event: Union[Message, CallbackQuery], state: FSMContext, user: Any):
    try:
        messages_ids = []
        await state.clear()

        async with async_session_maker() as session:
            users_car = await CarsRepository.find_one_or_none(session, user_id=user.id)

        lets_register_text = (
            "Для того, чтобы мы смогли зарегистрировать Вашу машину, "
            "напишите, пожалуйста, её <b>марку</b>. <i>Например, Lada</i>\n"
            "\n"
            "Чтобы информация была корректной, сверьте ее со списком "
            "машин, который будет по ссылке ниже\n"
            "\n"
            "<blockquote>"
            "<i>Настоятельно прошу Вас действовать <b>по инструкциям</b>\n"
            "Это позволит мне <b>корректно</b> зарегистрировать Вашу машину для дальнейшей работы</i>"
            "</blockquote>"
        )

        if isinstance(event, Message):
            await event.delete()

            if not users_car:
                await event.answer(lets_register_text, reply_markup=car_list())
                await state.set_state(SignupUserCarStates.brand)
                return

            await event.answer(
                text="Ваша машина зарегистрирована у нас. Это она, верно?\n"
                     "\n"
                     "<blockquote>"
                     f"<b>🔻 Брэнд:</b> {users_car.brand_name}\n"
                     f"<b>🔻 Марка:</b> {users_car.model_name}\n"
                     f"<b>🔻 Модификация:</b> {users_car.gen_name}\n"
                     f"<b>🔻 Год выпуска:</b> {users_car.year} года\n"
                     f"<b>🔻 Пробег:</b> {users_car.mileage}"
                     "</blockquote>",
                reply_markup=car_info_confirm()
            )
            await state.set_state(UpdateCarInfo.confirm_info)

        if isinstance(event, CallbackQuery):
            await event.message.delete()

            if not users_car:
                await event.message.edit_text(lets_register_text, reply_markup=car_list())
                await state.set_state(SignupUserCarStates.brand)
                return

            await event.message.edit_text(
                text="Ваша машина зарегистрирована у нас. Это она, верно?\n"
                     "\n"
                     "<blockquote>"
                     f"<b>🔻 Брэнд:</b> {users_car.brand_name}\n"
                     f"<b>🔻 Марка:</b> {users_car.model_name}\n"
                     f"<b>🔻 Модификация:</b> {users_car.gen_name}\n"
                     f"<b>🔻 Год выпуска:</b> {users_car.year} года\n"
                     f"<b>🔻 Пробег:</b> {users_car.mileage}"
                     "</blockquote>",
                reply_markup=car_info_confirm()
            )
            await state.set_state(UpdateCarInfo.confirm_info)
    except Exception as e:
        logger.error(f"Car: {e}")
        await event.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.brand)
async def get_model(message: Message, state: FSMContext):
    try:
        await message.answer("Отлично, теперь напишите, пожалуйста, модель своей машины.")
        await state.set_state(SignupUserCarStates.model)
        await state.update_data(car_brand=message.text)
    except Exception as e:
        logger.error(f"Car Brand: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.model)
async def get_year(message: Message, state: FSMContext):
    try:
        await message.answer(
            "Хорошая модель. Далее год производства машины. "
            "Просто число, например, <b>2012</b>"
        )

        await state.set_state(SignupUserCarStates.year)
        await state.update_data(car_model=message.text)
    except Exception as e:
        logger.error(f"Car Model: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.year)
async def get_gen(message: Message, state: FSMContext):
    try:
        if len(message.text) > 4:
            await message.answer(
                text="❌ Был введён неверный год выпуска, "
                     "пожалуйста, введите корректное значение",
                reply_markup=retry_register_car
            )
            return

        await message.answer(
            text="Отлично, теперь, пожалуйста укажите <b>модификацию</b> Вашей машины ниже 👇\n"
                 "Например, модель и литраж двигателя\n"
                 "\n"
                 "<blockquote>"
                 "Напоминаю, чтобы написать корректную информацию, "
                 "<b>не забудьте свериться</b> со списком машин, который я "
                 "отправлял ранее, и данными по Вашей машине"
                 "</blockquote>",
            reply_markup=car_list()
        )
        await state.set_state(SignupUserCarStates.gen)
        await state.update_data(car_year=message.text)
    except Exception as e:
        logger.error(f"Car Year: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.gen)
async def get_mileage(message: Message, state: FSMContext):
    try:
        await message.answer(
            "Напишите, пожалуйста, пробег Вашей машины ниже 👇\n"
            "Напишите именно количество тысяч километров.\n"
            "Например, если у Вас <i>150.000 км</i>, тогда напишите, только <i>150</i>"
        )
        await state.set_state(SignupUserCarStates.mileage)
        await state.update_data(car_gen=message.text)
    except Exception as e:
        logger.error(f"Mileage: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.mileage)
async def register(message: Message, state: FSMContext, user: Any):
    try:
        car_brand = await state.get_value("car_brand")
        car_model = await state.get_value("car_model")
        car_year = int(await state.get_value("car_year"))
        car_gen = await state.get_value("car_gen")
        car_mileage = int(message.text)

        async with async_session_maker() as session:
            new_car = await CarsRepository.add(
                session=session,
                user_id=user.id,
                brand_name=car_brand,
                model_name=car_model,
                gen_name=car_gen,
                year=car_year,
                mileage=car_mileage
            )

        if not new_car:
            await message.answer(
                "❌ Ошибка регистрации автомобиля, пожалуйста, "
                "попробуйте снова или позднее"
            )
            return

        await message.answer(
            text=f"✅ Отлично! Ваша машина:\n"
                 f"\n"
                 f"<blockquote>"
                 f"<b>🔻 Брэнд:</b> {car_brand}\n"
                 f"<b>🔻 Марка:</b> {car_model}\n"
                 f"<b>🔻 Год выпуска:</b> {car_year} года\n"
                 f"<b>🔻 Модификация:</b> {car_gen}\n"
                 f"<b>🔻 Пробег:</b> {car_mileage}"
                 f"</blockquote>\n"
                 "\n"
                 "Теперь, когда у нас есть вся необходимая информация, "
                 "Вы можете начать пользоваться нашей системой 🙌",
            reply_markup=lets_solution
        )
    except Exception as e:
        logger.error(f"Register: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()
