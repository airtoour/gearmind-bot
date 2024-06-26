from aiogram import Bot, Dispatcher
from config import settings
import logging

# Инициализация бота при запуске
bot = Bot(token=settings.TOKEN, parse_mode='HTML')
dp = Dispatcher()

# Инициализация модуля логирования бота
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
