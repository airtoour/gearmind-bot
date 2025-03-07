from typing import Union, Any

from aiogram import Router, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram.states.signup_car import SignupUserCarStates
from telegram.keyboards.inline.inline import (
    prod_types,
    result_solution,
    first_param
)
from telegram.utils.utils import TABLES_TEXT_MAPPING

from logger import logger


router = Router(name="solution")


@router.message(Command("solution"))
@router.callback_query(F.data == "solution")
async def solution(event: Union[Message, CallbackQuery]):
    """Обработчик, запускающий процесс подбора запчастей"""
    try:
        text = (
            "Для того, чтобы я смог подобрать Вам нужную продукцию, "
            "выберите проблемную область своей машины ниже 👇"
        )

        if isinstance(event, Message):
            await event.delete()
            await event.answer(text=text, reply_markup=prod_types())
        else:
            await event.message.delete()
            await event.message.answer(text=text, reply_markup=prod_types())
    except (Exception, TelegramAPIError) as e:
        logger.error(f"Solution: {e}")
        await event.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.callback_query(F.data.startswith("table:"))
async def problem_field(callback: CallbackQuery, state: FSMContext):
    """Хендлер, обрабатывающий выбранный проблемный аспект"""
    try:
        aspect_name = callback.data.split(":")[-1]
        text = TABLES_TEXT_MAPPING.get(aspect_name, "")

        await callback.message.answer(text=text, reply_markup=first_param(aspect_name))

        await state.set_state(SignupUserCarStates.set_result)
        await state.update_data(aspect=aspect_name)
    except (Exception, TelegramAPIError) as e:
        logger.error(f"Problem_field: {e}")
        await callback.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

@router.callback_query(F.data.startswith("value:"))
async def set_result(callback: CallbackQuery, state: FSMContext, user: Any):
    """Хендлер, выдающий результаты обработки проблемы"""
    try:
        data = callback.data.split(":")[-1]
        aspect_name = await state.get_value("aspect")

        await callback.message.answer(
            text="Я поискал для Вас продукты, которые <b>могут подойти</b> для Вас, "
                 "можете взглянуть на них по сcылке ниже 👇\n"
                 "\n\n"
                 "<blockquote>"
                 "<b>❗️ НАСТОЯТЕЛЬНО РЕКОМЕНДУЕТСЯ ❗️</b>\n"
                 "\n"
                 "Перед тем, как приобрести необходимый компонент, "
                 "<b>пожалуйста</b>, проконсультируйтесь со специалистами,"
                 "<b><u>компетентными</u></b> по данному вопросу"
                 "</blockquote>",
            reply_markup=await result_solution(aspect_name, data, user)
        )
    except (Exception, TelegramAPIError) as e:
        logger.error(f"Set Result: {e}")
        await callback.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()
