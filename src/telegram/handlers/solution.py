from io import BytesIO
from typing import Union

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from db.db_config import async_session_maker
from db.models.prompts.repository import PromptsRepository

from telegram.keyboards.reply.reply import get_problem_keyboard
from telegram.states.solution import SolutionStates

from ai.openai_api import openai_client

from logger import logger


router = Router(name="Work With User`s Solution")


@router.message(Command("solution"))
@router.callback_query(F.data == "solution")
async def solution(event: Union[Message, CallbackQuery]):
    """Обработчик, запускающий процесс подбора запчастей"""
    try:
        text = (
            "Для того, чтобы я <b>понял с чем Вам помочь</b>, выберите "
            "ниже, пожалуйста <b>проблемную область</b> ниже 👇"
        )

        if isinstance(event, Message):
            await event.delete()
            await event.answer(text=text, reply_markup=get_problem_keyboard)
        else:
            await event.message.delete()
            await event.message.answer(text=text, reply_markup=get_problem_keyboard)
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
            "Хорошо! Отправьте, пожалуйста, <b>текстовое</b> или "
            "<b>голосовое</b> сообщение ниже, чтобы я смог Вам помочь 👇"
        )
        await state.set_state(SolutionStates.solution_type)
        await state.set_data({"type": message.text})
    except (Exception, TelegramAPIError) as e:
        logger.error(f"Problem Part: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


@router.message(
    SolutionStates.solution_type,
    F.content_type.in_([
        ContentType.AUDIO,
        ContentType.TEXT
    ])
)
async def process_content(message: Message, state: FSMContext):
    file_info = None
    file_data = BytesIO()

    try:
        prompt_type = await state.get_value("type")

        async with async_session_maker() as session:
            prompt = await PromptsRepository.find_one_or_none(
                session, type=prompt_type[2:]
            )

        message_types = {
            "text": message.text,
            "audio": message.audio
        }

        for message_type, content in message_types.items():
            if message_type == "audio":
                if content:
                    file_info = await message.bot.get_file(message.audio.file_id)

                if not file_info:
                    await message.reply("<b>Неподдерживаемый</b> формат медиа-файла")
                    return

                try:
                    await message.bot.download_file(file_info.file_path, destination=file_data)
                    file_data.seek(0)
                except Exception as e:
                    logger.error(f"Ошибка при сохранении файла: {e}")
                    await message.reply(
                        "<b>Не получилось сохранить</b> Ваши файлы, "
                        "<i>попробуйте снова</i>"
                    )
                    return

                response = await openai_client.audio(prompt.text, file_data)

                if not response:
                    await message.answer(
                        "Произошла ошибка на стороне помощника!\n"
                        "Пожалуйста, попробуйте снова или позже!"
                    )
                    return

                await message.answer(str(response), reply_markup=ReplyKeyboardRemove())
            else:
                if content:
                    response = await openai_client.create(prompt.text, content)
                    await message.answer(str(response), reply_markup=ReplyKeyboardRemove())

            break
    except (Exception, TelegramAPIError) as e:
        logger.error(f"Process Content: {e}")
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()
