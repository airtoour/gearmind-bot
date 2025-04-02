from typing import Any, List

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession
from db.models import CarsRepository

from telegram.keyboards.inline.inline import car_info
from telegram.states.update_car_info import UpdateCarInfo

from logger import logger


router = Router(name="Fix Info of User`s Car")


@router.message(UpdateCarInfo.confirm_info)
async def confirm_car(message: Message, state: FSMContext, user: Any, session: AsyncSession):
    try:
        # Получаем список с ID сообщений на удаление
        messages_ids: List[int] = await state.get_value("messages_ids")

        # Записываем в список ответ "Да" или "Нет"
        messages_ids.append(message.message_id)

        for message_id in messages_ids:
            await message.bot.delete_message(message.chat.id, message_id)

        if message.text == "✅ Всё верно":
            await message.answer(
                "Я рад! 😊\n"
                "Если у Вас больше <b>нет</b> вопросов, связанных с Вашим автомобилем, "
                "то выберите, пожалуйста, команду <b>в Меню слева снизу</b>"
            )

        elif message.text == "❌ Не верно":
            car = await CarsRepository.find_one_or_none(session, user_id=user.id)

            await message.answer(
                text="Оу, что именно не так в названии Вашей машины?\n"
                     "Выберите <b>необходимую часть</b> Вашего автомобиля ниже ",
                reply_markup=await car_info(car)
            )

        else:
            if message.text.startswith("/"):
                await message.answer("Окей, переключаемся...")
    except Exception as e:
        logger.error(f"Confirm Car: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."""
        )
    finally:
        await state.clear()


@router.callback_query(F.data.startswith("info:"))
async def problem_parts(callback: CallbackQuery, state: FSMContext):
    try:
        field = callback.data.split(":")[1]
        value = callback.data.split(":")[-1]

        await callback.message.answer(
            f"Очень жаль, что информация оказалась неверной 😔\n\n"
            f"Давайте <b>изменим</b> эту часть для корректности\n"
            f"Напишите, пожалуйста, ниже <b>новое</b> значение 👇\n\n"
            f"<b>Текущее значение</b>: {value}"
        )
        await state.set_state(UpdateCarInfo.correct_part)
        await state.update_data(problem_field=field)
    except Exception as e:
        logger.error(f"Problem Parts: {e}")
        await callback.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


@router.message(UpdateCarInfo.correct_part)
async def update_part(message: Message, state: FSMContext, user: Any, session: AsyncSession):
    try:
        problem_field = await state.get_value("problem_field")
        new_value = message.text

        data = {problem_field: new_value}

        await CarsRepository.update(
            session,
            CarsRepository.model.user_id == user.id,
            **data
        )

        await message.edit_text(
            "Всё! Поправили. Надеюсь, такого больше не случится, успехов!"
        )
    except Exception as e:
        logger.error(f"Update Part: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()
