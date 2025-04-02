
from typing import Any, Union

from aiogram import Router, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext

from ai import yandex
from db.db_config import async_session_maker
from db.models.scores.repository import ScoresRepository
from services.process_ai_requests import RequestAIService

from telegram.keyboards.inline.inline import score_result
from telegram.keyboards.reply.reply import get_problem_keyboard
from telegram.states.solution import SolutionStates

from logger import logger


router = Router(name="Work With User`s Solution")


@router.message(Command("solution"))
@router.callback_query(F.data == "solution")
async def solution(event: Union[Message, CallbackQuery]):
    """Обработчик, запускающий процесс подбора запчастей"""
    message = None

    try:
        if isinstance(event, Message):
            message = event
        if isinstance(event, CallbackQuery):
            message = event.message

        await message.delete()
        await message.answer(
            text="Для того, чтобы я <b>понял с чем Вам помочь</b>, выберите, "
                 "пожалуйста, <b>проблемную область</b> ниже 👇",
            reply_markup=get_problem_keyboard
        )

    except (Exception, TelegramAPIError) as e:
        logger.error(f"Solution: {e}")
        await event.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


@router.message(F.text.in_(["🛞 Запчасти", "📿 Аксессуары", "🛢 Жидкости для авто"]))
async def problem_part(message: Message, state: FSMContext):
    try:
        await message.answer(
            "Хорошо! Отправьте, пожалуйста, <b>сообщение</b> "
            "ниже, чтобы я смог Вам помочь 👇\n"
            "\n"
            "<blockquote>"
            "<i>Пожалуйста, опишите, ситуацию чётко, ёмко и подробно "
            "настолько, насколько это возможно</i>"
            "</blockquote>"
        )
        await state.set_state(SolutionStates.solution_type)
        await state.set_data({"type": message.text})
    except (Exception, TelegramAPIError) as e:
        logger.error(f"Problem Part: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


@router.message(SolutionStates.solution_type)
async def process_content(message: Message, state: FSMContext, user: Any):
    try:
        working = await message.answer("<i>Внимательно изучаю Ваш запрос...</i>")

        prompt_type = await state.get_value("type")

        ai_service = RequestAIService(
            yandex, message.text, prompt_type[2:], user
        )

        result, request_id = await ai_service.create()

        await message.bot.delete_message(message.chat.id, working.message_id)

        if not result:
            await message.answer(
                "Произошла <b>ошибка при получении результата</b>, "
                "пожалуйста, попробуйте позже или ещё раз"
            )
            await state.clear()
            return

        # Отправляем ответ от ИИ пользователю
        await message.answer(
            f"{result}\n\n"
            f"<i>Хорошего Вам дня</i> ☀️\n\n"
            f"<b>Ваша команда GearMind</b> 🚗"
        )

        await message.answer(
            text="Оцените, пожалуйста, ответ от <b>1</b> до <b>5</b> ⭐️",
            reply_markup=score_result
        )
        await state.update_data(request_id=request_id)
    except (Exception, TelegramAPIError) as e:
        logger.error(f"Process Content: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
        await state.clear()


@router.callback_query(F.data.startswith("score:"))
async def process_score_result(callback: CallbackQuery, state: FSMContext, user: Any):
    try:
        # Получение оценки от пользователя
        score = int(callback.data.split(":")[-1])

        # Получение ID запроса, для сохранения в БД
        request_id = await state.get_value("request_id")

        # Записываем оценку в БД
        async with async_session_maker() as session:
            added_score = await ScoresRepository.add(
                session, request_id=request_id, user_id=user.id, score=score
            )

        # Если не получилось сохранить оценку
        if not added_score:
            await callback.message.edit_text(
                "Произошла ошибка <b>сохранении</b> Вашей <b>оценки</b>, "
                "приносим, свои извинения..."
            )
            return

        # Оповещаем пользователя об успешном сохранении оценки
        await callback.message.edit_text(f"<b>Ваша оценка</b>: {score} ⭐️")

        await callback.message.answer(
            text="Спасибо больше Вам за эту оценку ❤️\n"
                 "Мы стараемся сделать сервис <b>как можно лучше</b> 😎",
            reply_markup=ReplyKeyboardRemove()
        )
    except (Exception, TelegramAPIError) as e:
        logger.error(f"Process Score: {e}")
        await callback.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()
