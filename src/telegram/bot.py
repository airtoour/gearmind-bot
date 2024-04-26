from aiogram import Bot, Dispatcher
from config import config


bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp = Dispatcher()
