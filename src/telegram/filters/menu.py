from aiogram import Bot
from aiogram.types import BotCommand

from src.telegram.lexicon.lexicon import LEXICON_MENU_COMMANDS
from get_env import get_env

bot = Bot(token=get_env("TOKEN"),parse_mode='HTML')

# Кнопка меню, которая упаравляет основным функционалом
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description) for command, description in LEXICON_MENU_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu_commands)
