from typing import Union, Any

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from db.models.cars.repository import CarsRepository

from telegram.bot import bot
from telegram.states.signup_car import SignupUserCarStates
from telegram.states.update_car_info import UpdateCarInfo
from telegram.keyboards.reply.reply import car_info_confirm
from telegram.keyboards.inline.inline import car_list, lets_solution, retry_register_car

from logger import logger


router = Router(name="car")


@router.message(Command("car"))
@router.callback_query(F.data.in_(["car", "retry_register_car"]))
async def car(event: Union[Message, CallbackQuery], state: FSMContext, user: Any):
    try:
        await state.clear()

        if isinstance(event, Message):
            await event.delete()

        if isinstance(event, CallbackQuery):
            await event.message.delete()

        users_car = await CarsRepository.find_one_or_none(user_id=user.id)

        if not users_car:
            await bot.send_message(
                chat_id=event.from_user.id,
                text="Для того, чтобы мы смогли зарегистрировать Вашу машину, "
                     "напишите, пожалуйста, её <b>марку</b>\n"
                     "\n"
                     "Чтобы информация была корректной, сверьте ее со списком "
                     "машин, который будет по ссылке ниже\n"
                     "\n"
                     "Настоятельно прошу Вас действовать <b>по инструкциям</b> кнопок\n"
                     "Это позволит мне <b>корректно</b> зарегистрировать Вашу машину для дальнейшей работы.",
                reply_markup=car_list()
            )
            await state.set_state(SignupUserCarStates.car_brand)
            return

        await bot.send_message(
            chat_id=event.from_user.id,
            text="Ваша машина зарегистрирована у нас. Это она, верно?\n"
                 "\n"
                 "<blockquote>"
                 f"<b>🔻 Брэнд:</b> {users_car.brand_name}\n"
                 f"<b>🔻 Марка:</b> {users_car.model_name}\n"
                 f"<b>🔻 Модификация:</b> {users_car.gen_name}\n"
                 f"<b>🔻 Год выпуска:</b> {users_car.year} года"
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

@router.message(SignupUserCarStates.car_brand)
async def car_brand(message: Message, state: FSMContext):
    try:
        await message.answer("Отлично, теперь напишите, пожалуйста, модель своей машины.")
        await state.set_state(SignupUserCarStates.car_model)
        await state.update_data(car_brand=message.text)
    except Exception as e:
        logger.error(f"Car Brand: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.car_model)
async def car_model(message: Message, state: FSMContext):
    try:
        await message.answer(
            "Хорошая модель. Далее год производства машины. "
            "Просто число, например, 2012."
        )

        await state.set_state(SignupUserCarStates.car_year)
        await state.update_data(car_model=message.text)
    except Exception as e:
        logger.error(f"Car Model: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.car_year)
async def car_year(message: Message, state: FSMContext):
    try:
        if len(message.text) > 4:
            await message.answer(
                text="❌ Был введён неверный год выпуска, "
                     "пожалуйста, введите корректное значение",
                reply_markup=retry_register_car
            )
            return

        await message.answer(
            text="И самое главное, это модификация.\n"
                 "\n"
                 "<i>Напоминаю, чтобы написать корректную информацию, "
                 "не забудьте свериться со списком машин, который я "
                 "отправлял ранее, и данными по Вашей машине</i>",
            reply_markup=car_list()
        )
        await state.set_state(SignupUserCarStates.car_gen)
        await state.update_data(car_year=message.text)
    except Exception as e:
        logger.error(f"Car Year: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.car_gen)
async def register(message: Message, state: FSMContext, user: Any):
    try:
        brand = await state.get_value("car_brand")
        model = await state.get_value("car_model")
        gen = message.text
        year = await state.get_value("car_year")

        await CarsRepository.add(
            user_id=user.id,
            brand_name=brand,
            model_name=model,
            gen_name=gen,
            year=int(year)
        )

        await message.answer(
            text=f"✅ Отлично!\n"
                 f"Ваша машина: <b>{brand} {model} {gen} {year} года</b>\n"
                 "\n"
                 "Теперь, когда у нас есть вся необходимая информация, "
                 "Вы можете начать пользоваться моей системой по кнопке ниже",
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
