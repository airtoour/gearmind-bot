from aiogram import F
from aiogram.filters import CommandStart, Command

from src.telegram.bot import bot, dp
from src.telegram.filters.menu import set_main_menu
from src.telegram.states import UserStates

from src.telegram.utils.commands.start import start, confirm_signup
from src.telegram.handlers.support import support
from src.telegram.handlers.order import order, first_vote, second_vote, check_order, third_vote


if __name__ == '__main__':
    dp.startup.register(set_main_menu)

    # Регистрация обработчиков, связанных с командой /start
    dp.message.register(start, CommandStart())
    dp.message.register(confirm_signup, UserStates.confirm_signup)

    # Регистрация обработчиков, связанных с командой /order
    dp.message.register(order, Command('order'))
    dp.message.register(first_vote, F.text.lower() == "заказать")
    dp.message.register(second_vote, F.text.lower() == "проверить свой заказ")
    dp.message.register(check_order, UserStates.check_order)
    dp.message.register(third_vote, F.text.lower() == "помощь")

    # Регистрация обработчиков, связанных с командой /social

    # Регистрация обработчиков, связанных с командой /support
    dp.message.register(support, Command('support'))

    dp.run_polling(bot)
