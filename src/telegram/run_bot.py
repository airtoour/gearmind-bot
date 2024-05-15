# from aiogram import F
from aiogram.filters import CommandStart, Command

# from src.db.db import app, db
from src.db.db import engine, Base
from src.telegram.bot import bot, dp
from src.telegram.filters.menu import set_main_menu
from src.telegram.states import UserStates

from src.telegram.utils.commands.start import start
from src.telegram.handlers.support import support
# from src.telegram.handlers.order import order, first_vote, second_vote, check_order, third_vote
from src.telegram.handlers.social import social
from src.telegram.handlers.car import car, register

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     print("К базе подключились")

    Base.metadata.create_all(engine)

    # Регистрация кнопки меню в чате
    dp.startup.register(set_main_menu)

    # Регистрация обработчиков, связанных с командой /start
    dp.message.register(start, CommandStart())
    # dp.message.register(phone, UserStates.user_phone)
    # dp.message.register(city, UserStates.user_city)

    # Регистрация обработчиков, связанных с командой /car
    dp.message.register(car, Command('car'))
    dp.message.register(register, UserStates.car_register)

    # Регистрация обработчиков, связанных с командой /order
    # dp.message.register(order, Command('order'))
    # dp.message.register(first_vote, F.text.lower() == "заказать")
    # dp.message.register(second_vote, F.text.lower() == "проверить свой заказ")
    # dp.message.register(check_order, UserStates.check_order)
    # dp.message.register(third_vote, F.text.lower() == "помощь")

    # Регистрация обработчиков, связанных с командой /social
    dp.message.register(social, Command('social'))

    # Регистрация обработчиков, связанных с командой /support
    dp.message.register(support, Command('support'))

    dp.run_polling(bot)
