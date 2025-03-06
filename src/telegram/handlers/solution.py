from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.telegram.bot import bot
from src.telegram.states import UserStates
from src.telegram.keyboards.inline.inline import to_signup, prod_types, first_param, result_solution

<<<<<<< HEAD:src/telegram/handlers/solution.py
from db.models.users.repository import UsersRepository

from loguru import logger
=======
from db.users.repository import UsersRepository
from logger import logger
>>>>>>> dev:telegram/handlers/solution/solution.py


async def solution(message: Message):
    try:
<<<<<<< HEAD:src/telegram/handlers/solution.py
        user = awaitUsersRepository.get_by_tg(message.from_user.id)
=======
        user = await UsersRepository.get_by_tg(message.from_user.id)
>>>>>>> dev:telegram/handlers/solution/solution.py

        if user:
            await message.answer(
                "Для того, чтобы я смог подобрать тебе нужную продукцию, "
                "выбери область проблемной зоны своей машины ниже", reply_markup=prod_types()
            )
        else:
            await message.answer(
                "Для того, чтобы начать пользоваться этой функцией, нужно сначала Вас <b>зарегистрировать</b>.\n"
                "Это займёт буквально 1-2 минуты по кнопке ниже", reply_markup=to_signup()
            )
    except Exception as e:
        logger.error(f"Solution: {e}", exc_info=True)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


async def problem_field(callback_query: CallbackQuery, state: FSMContext):
    try:
        table = callback_query.data.replace("table:", "")
        sql_table = ""
        field = ""

        if table == "Масла":
            sql_table = "oils"
            field = "comment"
            await bot.send_message(
                callback_query.message.chat.id,
                "Выбери, пожалуйста вид масла, который ты чаще "
                "всего используешь для своей машины, чтобы подобрать новое ниже",
                reply_markup=first_param(sql_table)
            )
        if table == "Шины":
            sql_table = "busbars"
            field = "diameter"
            await bot.send_message(
                callback_query.message.chat.id,
                "Выбери, пожалуйста, диаметр твоих шин, чтобы подобрать новые ниже",
                reply_markup=first_param(sql_table)
            )
        if table == "Аккумуляторы":
            sql_table = "batteries"
            field = "capacity"
            await bot.send_message(
                callback_query.message.chat.id,
                "Выбери, пожалуйста, ёмкость аккумулятора, который, "
                "приемлем для твоей машины, чтобы подобрать подходящий ниже",
                reply_markup=first_param(sql_table)
            )
        if table == "Диски":
            sql_table = "disks"
            field = "diameter"
            await bot.send_message(
                callback_query.message.chat.id,
                "Выбери, пожалуйста, диаметр твоих дисков, чтобы подобрать новые ниже",
                reply_markup=first_param(sql_table)
            )

        await state.set_state(UserStates.set_result)
        await state.update_data(table=table)
        await state.update_data(field=field)
    except Exception as e:
        logger.error(f"Problem_field: {e}", exc_info=True)
        await bot.send_message(
            callback_query.message.chat.id,
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


async def set_result(callback_query: CallbackQuery, state: FSMContext):
    try:
        data = callback_query.data.replace('value:', '')
        get_data = await state.get_data()
        table_name = get_data.get('table')

        await bot.send_message(
            callback_query.from_user.id,
            "Я поискал для Вас продукты, которые Вам необходимы, можете взглянуть на них по сcылке ниже\n"
            "\n"
            "<b>P.S НАСТОЯТЕЛЬНО РЕКОМЕНДУЕТСЯ!!!</b>\n"
            "Перед тем, как приобрести необходимый компонент, пожалуйста, проконсультируйтесь со специалистами,"
            "компетентными в данном вопросе.",
            reply_markup = await result_solution(table_name, data, callback_query.from_user.id)
        )
    except Exception as e:
        logger.error(f"Set Result: {e}", exc_info=True)
        await bot.send_message(
            callback_query.message.chat.id,
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()
