from typing import Dict

from aiogram import Bot
from aiogram.types import BotCommand


MENU_COMMANDS: Dict[str, str] = {
    "/car": "Зарегистрировать свою машину",
    "/solution": "У меня проблема",
    "/social": "Другие социальные сети и сайт",
    "/help": "Помощь"
}


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in MENU_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu_commands)
