import asyncio
from typing import Union, Any, List

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
from db.models import CarsRepository

from telegram.handlers.car.fix_info import router as fix_info_cars
from telegram.states.signup_car import SignupUserCarStates
from telegram.states.update_car_info import UpdateCarInfo
from telegram.keyboards.reply.reply import car_info_confirm
from telegram.keyboards.inline.inline import (
    car_list,
    lets_solution,
    retry_register_car
)

from logger import logger


# Создаем роутер для работы с Автомобилем пользователя
router = Router(name="Work with User`s Car")

# Добавляем к этому роутеру роутер работы с информацией Автомобиля
router.include_router(fix_info_cars)


@router.message(Command("car"))
@router.callback_query(F.data.in_(["car", "retry_register_car"]))
async def car(event: Union[Message, CallbackQuery], state: FSMContext, user: Any, session: AsyncSession):
    """Обработчик команды /car и кнопки car, а также возвращения регистрации машины к началу"""
    message = None

    try:
        if isinstance(event, Message):
            message = event
        if isinstance(event, CallbackQuery):
            message = event.message

        # Создаём список сообщений на удаление
        messages_ids = []

        # Очищаем все состояния для корректной обработки
        await state.clear()

        # Ищем автомобиль пользователя
        users_car = await CarsRepository.find_one_or_none(session, user_id=user.id)

        # Удаляем предыдущее сообщение
        await message.delete()

        if users_car:
            # Показываем пользователю информацию о его автомобиле
            exists_car_message = await message.answer(
                text="Ваша машина зарегистрирована у нас. Это она, верно?\n\n"
                     f"<b>🔻 Брэнд:</b> {users_car.brand_name}\n"
                     f"<b>🔻 Марка:</b> {users_car.model_name}\n"
                     f"<b>🔻 Модификация:</b> {users_car.gen_name}\n"
                     f"<b>🔻 Год выпуска:</b> {users_car.year} года\n"
                     f"<b>🔻 Пробег:</b> {users_car.mileage}",
                reply_markup=car_info_confirm
            )
            await state.set_state(UpdateCarInfo.confirm_info)
            messages_ids.append(exists_car_message.message_id)
            await state.update_data(messages_ids=messages_ids)

            return

        # Если автомобиля не существует отправляем сообщение на его регистрацию
        to_register_car_message = await message.answer(
            text="⚠️ <b>Видим, что Вы ещё не регистрировали свой "
                 "автомобиль в нашей системе!</b>\n\n"
                 "Для того, чтобы мы смогли зарегистрировать Вашу машину, "
                 "напишите, пожалуйста, её <b>марку</b>. Например, <b>Lada</b>\n\n"
                 "Чтобы информация была корректной, сверьте ее со списком "
                 "машин, который будет по ссылке ниже\n\n"
                 "<blockquote>"
                 "<i>Настоятельно прошу Вас действовать <b>по инструкциям</b>\n"
                 "Это позволит нам <b>корректно</b> зарегистрировать Ваш "
                 "автомобиль для дальнейшей работы</i>"
                 "</blockquote>",
            reply_markup=car_list
        )

        # Записываем ID сообщения в список
        messages_ids.append(to_register_car_message.message_id)

        # Ставим состояние на регистрацию
        await state.set_state(SignupUserCarStates.brand)

        # Записываем список в состояние
        await state.update_data(messages_ids=messages_ids)
    except Exception as e:
        logger.error(f"Car: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.brand)
async def get_model(message: Message, state: FSMContext):
    try:
        # Получаем текущее состояние
        messages_ids: List[int] = await state.get_value("messages_ids")

        # Отправляем запрос на получение модели автомобиля
        get_model_message = await message.answer(
            "Отлично, теперь напишите, пожалуйста, "
            "<b>модель</b> своей машины ниже 👇"
        )

        messages_ids.append(message.message_id)
        messages_ids.append(get_model_message.message_id)

        await state.set_state(SignupUserCarStates.model)
        await state.update_data(car_brand=message.text, messages_ids=messages_ids)
    except Exception as e:
        logger.error(f"Car Brand: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


@router.message(SignupUserCarStates.model)
async def get_year(message: Message, state: FSMContext):
    try:
        # Получаем текущее состояние списка
        messages_ids: List[int] = await state.get_value("messages_ids")

        # Отправляем запрос на получение года производства его автомобиля
        get_year_message = await message.answer(
            "Хорошая модель. Далее год производства машины. "
            "Просто число, например, <b>2012</b>"
        )

        messages_ids.append(message.message_id)
        messages_ids.append(get_year_message.message_id)

        await state.set_state(SignupUserCarStates.year)
        await state.update_data(car_model=message.text, messages_ids=messages_ids)
    except Exception as e:
        logger.error(f"Car Model: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.year)
async def get_gen(message: Message, state: FSMContext):
    """Хендлер, обрабатывающий запрос на получение модификаций автомобиля"""
    try:
        messages_ids: List[int] = await state.get_value("messages_ids")

        # Если был введён неверный по формату год выпуска
        if (len(message.text) > 4 or len(message.text) < 4) or (
            message.text[0] == "2"
            and message.text[1].isdigit()
            and int(message.text[1]) > 0
        ):
            bad_year_message = await message.answer(
                text="❌ Был год выпуска был введён в не правильном формате, "
                     "пожалуйста, введите корректное значение\n\n"
                     "<blockquote><b><i>"
                     "К сожалению, придётся начать весь процесс заново.\n"
                     "Мы работаем над этим, просим извинения за неудобства"
                     "</i></b></blockquote>",
                reply_markup=retry_register_car
            )

            messages_ids.append(message.message_id)
            messages_ids.append(bad_year_message.message_id)

            await state.set_state(SignupUserCarStates.gen)
            await state.update_data(messages_ids=messages_ids)

            return

        get_gen_message = await message.answer(
            text="Отлично, теперь, пожалуйста укажите <b>модификацию</b>, "
                 "<b>комплектацию</b> и т.п. Вашей машины ниже 👇\n\n"
                 "<blockquote>"
                 "Напоминаю, чтобы написать корректную информацию, "
                 "<b>не забудьте свериться</b> со информацией, которую мы "
                 "отправляли Вам ранее (кнопка), и данными по Вашей машине"
                 "</blockquote>",
            reply_markup=car_list
        )

        messages_ids.append(message.message_id)
        messages_ids.append(get_gen_message.message_id)

        await state.set_state(SignupUserCarStates.gen)
        await state.update_data(car_year=message.text, messages_ids=messages_ids)
    except Exception as e:
        logger.error(f"Car Year: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.gen)
async def get_mileage(message: Message, state: FSMContext):
    try:
        messages_ids: List[int] = await state.get_value("messages_ids")

        get_mileage_message = await message.answer(
            "Напишите, пожалуйста, пробег Вашей машины ниже 👇\n"
            "Напишите именно количество тысяч километров.\n"
            "Например, если у Вас <i>150.000 км</i>, тогда напишите, только <i>150</i>"
        )

        messages_ids.append(message.message_id)
        messages_ids.append(get_mileage_message.message_id)

        await state.set_state(SignupUserCarStates.mileage)
        await state.update_data(car_gen=message.text, messages_ids=messages_ids)
    except Exception as e:
        logger.error(f"Mileage: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.message(SignupUserCarStates.mileage)
async def register(message: Message, state: FSMContext, user: Any, session: AsyncSession):
    try:
        messages_ids = await state.get_value("messages_ids")

        car_brand = await state.get_value("car_brand")
        car_model = await state.get_value("car_model")
        car_year = int(await state.get_value("car_year"))
        car_gen = await state.get_value("car_gen")
        car_mileage = int(message.text)

        # Заводим таску на удаление сообщений
        delete_messages_task = [
            message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=message_id
            ) for message_id in messages_ids
        ]

        added_car = CarsRepository.add(
            session=session,
            user_id=user.id,
            brand_name=car_brand,
            model_name=car_model,
            gen_name=car_gen,
            year=car_year,
            mileage=car_mileage,
            full=f"{car_brand} {car_model} "
                 f"{car_gen} {car_year} года с "
                 f"пробегом {car_mileage} тыс. км"
        )

        try:
            # Выполняем таски
            results = await asyncio.gather(
                *delete_messages_task,
                added_car,
                return_exceptions=True
            )
        except Exception as e:
            logger.error(
                f"При выполнении тасок при создании "
                f"инцидента произошла ошибка: {e}"
            )
            return

        messages_ids.clear()

        new_car = results[-1]

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
