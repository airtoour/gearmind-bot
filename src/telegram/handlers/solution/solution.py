from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy import MetaData, Table, select
from src.db.db import engine

from src.telegram.bot import logger, bot
from src.telegram.states import UserStates
from src.telegram.keyboards.inline.inline import to_signup, prod_types, first_param, result_solution

from src.db.models.models import Users


async def solution(message: Message):
    try:
        user = Users.get_user_by_tg(message.from_user.id)

        if user:
            await message.answer(
                "Для того, чтобы я смог подобрать тебе нужную продукцию, "
                "выбери область проблемной зоны своей машины ниже", reply_markup=prod_types()
            )
        else:
            await message.answer(
                "Для того, чтобы начать пользоваться этой функцией, нужно сначала <b>тебя зарегистрировать</b>.\n"
                "Это займёт буквально 1-2 минуты по кнопке ниже", reply_markup=to_signup()
            )
    except Exception as e:
        logger.exception("solution", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


async def problem_field(callback_query: CallbackQuery, state: FSMContext):
    try:
        table = callback_query.data.replace('table:', '')
        sql_table = ""
        field = ""

        if table == 'Масла':
            sql_table = 'oils'
            field = 'comment'
            await bot.send_message(
                callback_query.message.chat.id,
                "Выбери, пожалуйста вид масла, который ты чаще "
                "всего используешь для своей машины, чтобы подобрать новое ниже",
                reply_markup=first_param(sql_table)
            )
        if table == 'Шины':
            sql_table = 'busbars'
            field = 'diameter'
            await bot.send_message(
                callback_query.message.chat.id,
                "Выбери, пожалуйста, диаметр твоих шин, чтобы подобрать новые ниже",
                reply_markup=first_param(sql_table)
            )
        if table == 'Аккумуляторы':
            sql_table = 'batteries'
            field = 'capacity'
            await bot.send_message(
                callback_query.message.chat.id,
                "Выбери, пожалуйста, ёмкость аккумулятора, который, "
                "приемлем для твоей машины, чтобы подобрать подходящий ниже",
                reply_markup=first_param(sql_table)
            )
        if table == 'Диски':
            sql_table = 'disks'
            field = 'diameter'
            await bot.send_message(
                callback_query.message.chat.id,
                "Выбери, пожалуйста, диаметр твоих дисков, чтобы подобрать новые ниже",
                reply_markup=first_param(sql_table)
            )

        await state.set_state(UserStates.set_result)
        await state.update_data(table=sql_table)
        await state.update_data(field=field)
    except Exception as e:
        logger.exception("problem_field", e)
        await bot.send_message(
            callback_query.message.chat.id,
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )


async def set_result(callback_query: CallbackQuery, state: FSMContext):
    try:
        metadata = MetaData()
        value = callback_query.data.replace('value:', '')

        get_data = await state.get_data()
        table_name = get_data.get('table')
        field = get_data.get('field')

        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table).where(getattr(table.c, field) == value)

        names = []
        with engine.connect() as connection:
            result = connection.execute(stmt)
            for row in result:
                names.append(row[2])
            print(names)

            await bot.send_message(
                callback_query.from_user.id,
                "Я поискал для тебя продукты, которые тебе необходимы, можешь взглянуть на них по сcылке ниже",
                reply_markup=result_solution(names)
            )
    except Exception as e:
        logger.exception("set_result", e)
        await bot.send_message(
            callback_query.message.chat.id,
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()