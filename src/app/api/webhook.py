from contextlib import asynccontextmanager

from aiogram.types import Update
from fastapi import FastAPI, APIRouter
from telegram.bot import bot, dp

from config import settings


router = APIRouter(tags=["Webhook"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Вебхук обработки обновлений от Aiogram"""

    # Ставим webhook на бота
    await bot.set_webhook(
        url=settings.get_webhook_url(),
        allowed_updates=dp.resolve_used_update_types()
    )

    # Генерируем обработку обновлений
    yield

    # Удаляем вебхук после завершения работы приложения
    await bot.delete_webhook()


@router.post("/webhook")
async def webhook(update: Update) -> None:
    """Webhook для обработки обновлений в TelegramBot"""
    await dp.feed_update(bot, update)
    return {"status": "ok"}
