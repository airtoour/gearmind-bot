import asyncio

from aiogram.filters import CommandStart, Command

from src.telegram.bot import bot, dp
from src.telegram.filters.menu import set_main_menu
from src.telegram.states import UserStates

from src.telegram.utils.commands.start import start
from src.telegram.utils.commands.signup import signup, get_phone
from src.telegram.handlers.social import social
from src.telegram.handlers.car import (car_command, car_button, confirm_car, problem_parts, update_part,
                                   car_brand, car_model, car_year, register)
from src.telegram.handlers.solution import solution, problem_field, set_result

from loguru import logger


async def main():
    await set_main_menu(bot)

    dp.message.register(start, CommandStart())

    dp.callback_query.register(signup, lambda c: c.data == "/signup")
    dp.message.register(get_phone, UserStates.phone)

    dp.message.register(car_command, Command("car"))
    dp.callback_query.register(car_button, lambda c: c.data == "/car")
    dp.message.register(confirm_car, UserStates.confirm_info)
    dp.callback_query.register(problem_parts, lambda c: c.data.startswith("info"))
    dp.message.register(update_part, UserStates.correct_part)
    dp.message.register(car_brand, UserStates.car_brand)
    dp.message.register(car_model, UserStates.car_model)
    dp.message.register(car_year, UserStates.car_year)
    dp.message.register(register, UserStates.car_gen)

    dp.message.register(solution, Command("solution"))
    dp.callback_query.register(problem_field, lambda c: c.data.startswith("table"))
    dp.callback_query.register(set_result, lambda c: c.data.startswith("value"))

    dp.message.register(social, Command("social"))

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.critical("Exiting bot...")
    finally:
        logger.info("Done")
