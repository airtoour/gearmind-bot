from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from get_env import get_env

bot = Bot(token='7080875225:AAEBnUoA_feRBQ5FwIGOPyAOhrCmeuh6Ic8')
storage = MemoryStorage()
dp = Dispatcher()
