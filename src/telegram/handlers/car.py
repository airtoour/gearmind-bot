from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.telegram.bot import bot, logger
from src.telegram.states import UserStates
from src.telegram.keyboards.reply.reply import car_info_confirm
from src.telegram.keyboards.inline.inline import car_info, car_list, lets_solution, to_signup

from src.db.models.models import Cars, Users
from src.db.db import session


async def car(form_user_id: int, state: FSMContext):
    try:
        user = Users.get_user_by_tg(form_user_id)
        confirm = car_info_confirm()
        user_id = Users.get_user_id(form_user_id)
        car = Cars.get_car(user_id)

        if user:
            if car:
                await bot.send_message(
                    form_user_id,
                    "Твоя машина зарегистрирована у нас. Это она, верно?\n"
                    f"<b>{car.brand_name} {car.model_name} {car.gen_name} {car.year} года</b>", reply_markup=confirm
                )
                await state.set_state(UserStates.confirm_info)
            else:
                await bot.send_message(
                    form_user_id,
                    "Для того, чтобы я смог зарегистрировать твою машину, напиши, пожалуйста, "
                    "<b>марку</b> своей машины\n"
                    "Для того, чтобы информация была корректной, сверь ее со списком машин, "
                    "который будет по ссылке ниже\n"
                    "\n"
                    "Настоятельно прошу тебя действовать по инструкции, которые я указываю. Это позволит мне корректно "
                    "зарегистрировать твою машину для дальнейшей работы.",
                    reply_markup=car_list()
                )
                await state.set_state(UserStates.car_brand)
        else:
            await bot.send_message(
                form_user_id,
                "Для того, чтобы зарегистрировать свою машину, нужно сначала <b>тебя</b> зарегистрировать.\n"
                "Это займёт буквально 1-2 минуты по кнопке ниже", reply_markup=to_signup()
            )
    except Exception as e:
        logger.exception("car", e)
        await bot.send_message(
            form_user_id,
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

async def car_command(message: Message, state: FSMContext):
    await car(message.from_user.id, state)

async def car_button(callback_query: CallbackQuery, state: FSMContext):
    await car(callback_query.from_user.id, state)


async def confirm_car(message: Message, state: FSMContext):
    try:
        await state.update_data(answer=message.text)
        get_data = await state.get_data()
        answer = get_data.get('answer')

        if answer == "Всё верно":
            await message.answer(
                "Я рад! Если у тебя больше нет вопросов, связанных с машиной, "
                "то выбери интересующую тебя команду в меню команд"
            )
        elif answer == "Не верно":
            user_id = Users.get_user_id(message.from_user.id)
            problem_part = car_info(user_id)
            await message.answer(
                "Оу, что именно не так в названии твоей машины?\n"
                "Выбери необходимую часть, в которой проблема ниже", reply_markup=problem_part
            )
    except Exception as e:
        logger.exception("confirm_car", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."""
        )
    finally:
        await state.clear()

async def problem_parts(callback_query: CallbackQuery, state: FSMContext):
    try:
        identifier, field = callback_query.data.split(':')
        if identifier == 'info':
            await bot.send_message(
                callback_query.from_user.id,
                f"Очень жаль, что так получилось. Давай изменим эту часть для корректности.\n"
                f"Напиши ниже корректную информацию."
            )
            await state.update_data(problem_field=field)
            await state.set_state(UserStates.correct_part)
    except Exception as e:
        logger.exception("problem_parts", e)
        await bot.send_message(
            callback_query.from_user.id,
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

async def update_part(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        problem_field = data.get('problem_field')

        new_value = message.text
        user_id = Users.get_user_id(message.from_user.id)
        car = Cars.get_car(user_id)

        setattr(car, problem_field, new_value)

        session.commit()

        await message.answer(f"Всё! Поправили. Надеюсь такого больше не случится, успехов!")

    except Exception as e:
        logger.exception("update_part", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()


async def car_brand(message: Message, state: FSMContext):
    try:
        await message.answer("Отлично, теперь напиши, пожалуйста, модель своей машины.")
        await state.update_data(car_brand=message.text)
        await state.set_state(UserStates.car_model)
    except Exception as e:
        logger.exception("car_brand", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

async def car_model(message: Message, state: FSMContext):
    try:
        await message.answer("Хорошая модель. Далее год производства машины. Просто число, например, 2012.")
        await state.update_data(car_model=message.text)
        await state.set_state(UserStates.car_year)
    except Exception as e:
        logger.exception("car_model", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

async def car_year(message: Message, state: FSMContext):
    try:
        await message.answer(
            "И самое главное, это модификация. Напоминаю, чтобы написать корректную информацию, "
            "не забудь свериться со списком машин и данными по твоей машине", reply_markup=car_list()
        )
        await state.update_data(car_year=message.text)
        await state.set_state(UserStates.car_gen)
    except Exception as e:
        logger.exception("car_year", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

async def register(message: Message, state: FSMContext):
    try:
        await message.answer(
            "Спасибо большое за предоставленную информацию о своей машине. "
            "Это поможет тебе в решении проблем с машиной."
        )
        await state.update_data(car_gen=message.text)
        get_data = await state.get_data()

        brand = get_data.get('car_brand')
        model = get_data.get('car_model')
        gen = get_data.get('car_gen')
        year = get_data.get('car_year')

        Cars.car_register(brand, model, gen, year, message.from_user.id)

        await message.answer(
            "Теперь, когда у нас есть вся необходимая информация, "
            "ты можешь начать пользоваться моей системой по кнопке ниже.", reply_markup=lets_solution()
        )
    except Exception as e:
        logger.exception("register", e)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()