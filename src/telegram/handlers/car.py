from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.telegram.bot import bot
from src.telegram.states import UserStates
from src.telegram.keyboards.reply.reply import car_info_confirm
from src.telegram.keyboards.inline.inline import car_info, car_list, lets_solution, to_signup

<<<<<<< HEAD:src/telegram/handlers/car.py
from db.models.users.repository import UsersRepository
from db.models.cars.repository import CarsRepository
=======
from db.users.sync_repository import SyncUsersRepository
from db.cars.sync_repository import SyncCarsRepository
>>>>>>> dev:telegram/handlers/car.py

from loguru import logger


async def car(from_user_id: int, state: FSMContext):
    try:
<<<<<<< HEAD:src/telegram/handlers/car.py
        user = await UsersRepository.get_by_tg(form_user_id)
        confirm = car_info_confirm()
        user_id = await UsersRepository.find_by_id(form_user_id)
        users_car = await CarsRepository.find_one_or_none(user_id=user_id)

        if user and car:
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
=======
        user = SyncUsersRepository.find_one_or_none(tg_user_id=from_user_id)
        users_car = SyncCarsRepository.find_one_or_none(user_id=user.tg_user_id)

        if user:
            if users_car:
                await bot.send_message(
                    from_user_id,
                    "Ваша машина зарегистрирована у нас. Это она, верно?\n"
                    f"<b>{users_car.brand_name} {users_car.model_name} {users_car.gen_name} {users_car.year} года</b>",
                    reply_markup=car_info_confirm()
                )
                await state.set_state(UserStates.confirm_info)
            else:
                await bot.send_message(
                    from_user_id,
                    "Для того, чтобы я смог зарегистрировать твою машину, напишите, пожалуйста, "
                    "<b>марку</b> своей машины\n"
                    "Для того, чтобы информация была корректной, сверьте ее со списком машин, "
                    "который будет по ссылке ниже\n"
                    "\n"
                    "Настоятельно прошу Вас действовать по инструкции, которые я указываю. Это позволит мне корректно "
                    "зарегистрировать Вашу машину для дальнейшей работы.",
                    reply_markup=car_list()
                )
                await state.set_state(UserStates.car_brand)
>>>>>>> dev:telegram/handlers/car.py
        else:
            await bot.send_message(
                from_user_id,
                "Для того, чтобы зарегистрировать свою машину, нужно сначала <b>Вас</b> зарегистрировать.\n"
                "Это займёт буквально 1-2 минуты по кнопке ниже", reply_markup=to_signup()
            )
    except Exception as e:
        logger.error(f"Car: {e}", exc_info=True)
        await bot.send_message(
            from_user_id,
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
                "Я рад! Если у Вас больше нет вопросов, связанных с машиной, "
                "то выберите интересующую Вас команду в меню команд слева снизу"
            )
        elif answer == "Не верно":
<<<<<<< HEAD:src/telegram/handlers/car.py
            user_id = await UsersRepository.find_by_id(message.form_user.id)
            problem_part = car_info(user_id)
=======
            problem_part = car_info(message.from_user.id)
>>>>>>> dev:telegram/handlers/car.py
            await message.answer(
                "Оу, что именно не так в названии Вашей машины?\n"
                "Выберите необходимую часть, в которой проблема ниже", reply_markup=problem_part
            )
    except Exception as e:
        logger.error(f"Confirm Car: {e}", exc_info=True)
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
                f"Очень жаль, что так получилось. Давайте изменим эту часть для корректности.\n"
                f"Напишите ниже корректную информацию."
            )
            await state.update_data(problem_field=field)
            await state.set_state(UserStates.correct_part)
    except Exception as e:
        logger.error(f"Problem Parts: {e}", exc_info=True)
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
<<<<<<< HEAD:src/telegram/handlers/car.py
        user = await UsersRepository.find_by_id(message.form_user.id)

        await CarsRepository.update(user.id, problem_field, new_value)
=======

        SyncCarsRepository.update_car(message.from_user.id, problem_field, new_value)
>>>>>>> dev:telegram/handlers/car.py

        await message.answer(f"Всё! Поправили. Надеюсь, такого больше не случится, успехов!")

    except Exception as e:
        logger.error(f"Update Part: {e}", exc_info=True)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()


async def car_brand(message: Message, state: FSMContext):
    try:
        await message.answer("Отлично, теперь напишите, пожалуйста, модель своей машины.")
        await state.update_data(car_brand=message.text)
        await state.set_state(UserStates.car_model)
    except Exception as e:
        logger.error(f"Car Brand: {e}", exc_info=True)
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
        logger.error(f"Car Model: {e}", exc_info=True)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

async def car_year(message: Message, state: FSMContext):
    try:
        await message.answer(
            "И самое главное, это модификация. Напоминаю, чтобы написать корректную информацию, "
            "не забудьте свериться со списком машин и данными по Вашей машине", reply_markup=car_list()
        )
        await state.update_data(car_year=message.text)
        await state.set_state(UserStates.car_gen)
    except Exception as e:
        logger.error(f"Car Year: {e}", exc_info=True)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )

async def register(message: Message, state: FSMContext):
    try:
        await message.answer(
            "Спасибо большое за предоставленную информацию о своей машине. Это поможет Вам в дальнейшем."
        )
        await state.update_data(car_gen=message.text)
        get_data = await state.get_data()

        brand = get_data.get("car_brand")
        model = get_data.get("car_model")
        gen = get_data.get("car_gen")
        year = get_data.get("car_year")

<<<<<<< HEAD:src/telegram/handlers/car.py
        await CarsRepository.add(
            user_id=message.from_user.id,
            brand_name=brand,
            model_name=model,
            gen_name=gen,
            year=year
        )

        await message.answer(
            text=(
                "Теперь, когда у нас есть вся необходимая информация, "
                "ты можешь начать пользоваться моей системой по кнопке ниже."
            ),
            reply_markup=lets_solution
=======
        SyncCarsRepository.add_car(
            user_id = message.from_user.id,
            brand_name = brand,
            model_name = model,
            gen_name = gen,
            year = year
        )

        await message.answer(
            f"Отлично! Ваша машина: <b>{brand} {model} {gen} {year}</b>\n"
            "\n"
            "Теперь, когда у нас есть вся необходимая информация, "
            "Вы можете начать пользоваться моей системой по кнопке ниже.",
            reply_markup=lets_solution()
>>>>>>> dev:telegram/handlers/car.py
        )
    except Exception as e:
        logger.error(f"Register: {e}", exc_info=True)
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства..."
        )
    finally:
        await state.clear()
