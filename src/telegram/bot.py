from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import settings


bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
