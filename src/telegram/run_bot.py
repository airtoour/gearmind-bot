from src.telegram.bot import bot
from src.telegram.utils.commands import dp


if __name__ == '__main__':
    dp.run_polling(bot)

