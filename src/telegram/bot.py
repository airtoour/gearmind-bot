from aiogram import Bot, Dispatcher
from get_env import get_env


bot = Bot(token=get_env("TOKEN"))
dp = Dispatcher()
