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

from db.models import ScoresRepository
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.cars.repository import CarsRepository
from services.ai_service.find_products import FindProducts
from services.ai_service.process_requests import RequestAIService

from telegram.keyboards.inline.inline import score_result, products_ozon_keyboard
from telegram.keyboards.reply.reply import get_type_keyboard
from telegram.states.solution import SolutionStates

from logger import logger


# Определяем роутер процесса
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
            reply_markup=get_type_keyboard
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
async def process_content(message: Message, state: FSMContext, user: Any, session: AsyncSession):
    try:
        # Поиск автомобиля пользователя для использования дальше
        car = await CarsRepository.find_one_or_none(session, user_id=user.id)

        # Отправляем сообщение о том, что начали работу
        working = await message.answer("<i>Внимательно изучаю Ваш запрос...</i>")

        # Получаем тип промпта
        prompt_type = await state.get_value("type")

        # Определяем сервис работы с ИИ
        ai_service = RequestAIService(
            ai=yandex,
            request=message.text,
            prompt_type=prompt_type[2:],
            user=user,
            session=session
        )

        # Получаем ответ от ИИ
        result, request_id = await ai_service.create()

        # Удаляем сообщение о начале работы
        await message.bot.delete_message(message.chat.id, working.message_id)

        if not result:
            await message.answer(
                "Произошла <b>ошибка при получении результата</b>, "
                "пожалуйста, попробуйте позже или ещё раз"
            )
            await state.clear()
            return

        # Определяем сервис получения продуктов
        products = FindProducts(car, result)

        # Отправляем сообщение о поиске товаров на маркетплейсах
        finding = await message.answer("<i>Ищу на маркетплейсах...</i>")

        # Формируем названия товаров и ссылок
        products_data = products.get_urls_list()

        # Удаляем сообщение о поиске товаров
        await message.bot.delete_message(message.chat.id, finding.message_id)

        if not products_data:
            await message.answer(
                "Произошла ошибка <b>при поиске товаров на маркетплейсах</b>, "
                "пожалуйста, попробуйте позже или ещё раз"
            )

        # Отправляем ответ от ИИ пользователю
        await message.answer(result)

        # Отправляем сообщений с товарами
        await message.answer(
            text=f"Также мы <b>нашли</b> эти товары на маркетплейсе "
                 f"нашего <b>партнёра OZON</b> 👇\n\n"
                 f"<i>Хорошего Вам дня</i> ☀️",
            reply_markup=products_ozon_keyboard(products_data)
        )

        # Запрашиваем оценку от пользователя
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
async def process_score_result(callback: CallbackQuery, state: FSMContext, user: Any, session: AsyncSession):
    try:
        # Получение оценки от пользователя
        score = int(callback.data.split(":")[-1])

        # Получение ID запроса, для сохранения в БД
        request_id = await state.get_value("request_id")

        # Записываем оценку в БД
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
        await callback.message.edit_text(
            text=f"<b>Ваша оценка</b>: {score} ⭐️\n\n"
                 "Спасибо больше Вам за эту оценку ❤️\n"
                 "Мы стараемся сделать наш сервис <b>как можно лучше</b> 😎\n\n"
                 "<b>Ваша команда GearMind</b> 🚗",
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
