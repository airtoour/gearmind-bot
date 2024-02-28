from aiogram import Bot, Dispatcher
from src.settings import settings

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()