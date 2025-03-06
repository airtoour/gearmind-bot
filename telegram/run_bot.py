from aiogram.filters import CommandStart, Command

from db.db import Base, sync_engine
from telegram.bot import bot, dp
from telegram.filters.menu import set_main_menu
from telegram.states import UserStates

from telegram.utils.commands.start import start
from telegram.utils.commands.signup import signup, get_phone
from telegram.handlers.social import social
from telegram.handlers.car import (car_command, car_button, confirm_car, problem_parts, update_part,
                                   car_brand, car_model, car_year, register)
from telegram.handlers.solution.solution import solution, problem_field, set_result
from telegram.handlers.help import help_command


if __name__ == '__main__':
    Base.metadata.create_all(sync_engine)

    dp.startup.register(set_main_menu)

    dp.message.register(start, CommandStart())

    dp.callback_query.register(signup, lambda c: c.data == '/signup')
    dp.message.register(get_phone, UserStates.phone)

    dp.message.register(car_command, Command('car'))
    dp.callback_query.register(car_button, lambda c: c.data == '/car')
    dp.message.register(confirm_car, UserStates.confirm_info)
    dp.callback_query.register(problem_parts, lambda c: c.data.startswith('info'))
    dp.message.register(update_part, UserStates.correct_part)
    dp.message.register(car_brand, UserStates.car_brand)
    dp.message.register(car_model, UserStates.car_model)
    dp.message.register(car_year, UserStates.car_year)
    dp.message.register(register, UserStates.car_gen)

    dp.message.register(solution, Command('solution'))
    dp.callback_query.register(problem_field, lambda c: c.data.startswith('table'))
    dp.callback_query.register(set_result, lambda c: c.data.startswith('value'))

    dp.message.register(social, Command('social'))

    dp.message.register(help_command, Command('help'))

    dp.run_polling(bot)
