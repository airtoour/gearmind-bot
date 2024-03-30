from src.telegram.bot import bot, dp
from src.telegram.filters.menu import set_main_menu
from src.telegram.states import UserStates

from src.telegram.utils.commands.start import start, confirm_signup, CommandStart
from src.telegram.handlers.support import support, Command


if __name__ == '__main__':
    dp.startup.register(set_main_menu)

    # Регистрация обработчиков, связанных с командой /start
    dp.message.register(start, CommandStart())
    dp.message.register(confirm_signup, UserStates.confirm_signup)

    # Регистрация обработчиков, связанных с командой /order
    # Регистрация обработчиков, связанных с командой /check
    # Регистрация обработчиков, связанных с командой /description
    # Регистрация обработчиков, связанных с командой /social
    # Регистрация обработчиков, связанных с командой /faq

    # Регистрация обработчиков, связанных с командой /support
    dp.message.register(support, Command('support'))

    dp.run_polling(bot)
