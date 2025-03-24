from typing import Dict

from aiogram import Bot
from aiogram.types import BotCommand


COMMANDS: Dict[str, str] = {
    "/profile": "Мой профиль 🫅",
    "/car": "Работа с машиной 🚗",
    "/solution": "У меня проблема 🪲",
    "/social": "Другие социальные сети и сайт",
    "/help": "Помощь"
}


async def set_main_menu(bot: Bot):
    commands = [
        BotCommand(command=command, description=description)
        for command, description in COMMANDS.items()
    ]
    await bot.set_my_commands(commands)
