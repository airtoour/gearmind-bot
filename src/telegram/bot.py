import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from db.models.users.repository import UsersRepository
from telegram.middlewares.user_info import UserDataMiddleware

from config import settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

dp.update.middleware.register(UserDataMiddleware(repository=UsersRepository()))
