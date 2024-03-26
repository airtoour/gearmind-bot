from src.telegram.bot import bot
from src.telegram.utils.commands import dp
from src.telegram.filters.menu import set_main_menu

if __name__ == '__main__':
    dp.startup.register(set_main_menu)

    bot.delete_webhook(drop_pending_updates=True)
    dp.run_polling(bot)

