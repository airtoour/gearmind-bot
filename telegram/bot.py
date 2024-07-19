from aiogram import Bot, Dispatcher
from src.config import settings


bot = Bot(token=settings.TOKEN, parse_mode='HTML')
dp = Dispatcher()
