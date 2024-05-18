# from aiogram import F
from aiogram.filters import CommandStart, Command

# from src.db.db import app, db
from src.db.db import engine, Base
from src.telegram.bot import bot, dp
from src.telegram.filters.menu import set_main_menu
from src.telegram.states import UserStates

from src.telegram.utils.commands.start import start
from src.telegram.utils.commands.signup import signup, get_phone
from src.telegram.handlers.support import support
from src.telegram.handlers.social import social
from src.telegram.handlers.car import (car, confirm_car, problem_parts, update_part,
                                       car_brand, car_model, car_year, register)
from src.telegram.handlers.solution.solution import solution, problem_field, set_result


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("К базе подключились")

    # Регистрация кнопки меню в чате
    dp.startup.register(set_main_menu)

    # Регистрация обработчиков, связанных с командой /start
    dp.message.register(start, CommandStart())

    # Регистрация команды /signup
    dp.callback_query.register(signup, lambda c: c.data == '/signup')
    dp.message.register(get_phone, UserStates.phone)

    # Регистрация обработчиков, связанных с командой /car
    dp.message.register(car, Command('car'))
    dp.message.register(confirm_car, UserStates.confirm_info)
    dp.callback_query.register(problem_parts, lambda c: c.data.startswith('info'))
    dp.message.register(update_part, UserStates.correct_part)
    dp.message.register(car_brand, UserStates.car_brand)
    dp.message.register(car_model, UserStates.car_model)
    dp.message.register(car_year, UserStates.car_year)
    dp.message.register(register, UserStates.car_gen)

    # Регистрация обработчиков, связанных с командой /solution
    dp.message.register(solution, Command('solution'))
    dp.callback_query.register(problem_field, lambda c: c.data.startswith('table'))
    dp.callback_query.register(set_result, lambda c: c.data.startswith('value'))

    # Регистрация обработчиков, связанных с командой /social
    dp.message.register(social, Command('social'))

    # Регистрация обработчиков, связанных с командой /support
    dp.message.register(support, Command('support'))

    print("Бот работает")
    dp.run_polling(bot)
