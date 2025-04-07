from aiogram.types import Update
from fastapi import APIRouter
from telegram.bot import bot, dp


router = APIRouter(tags=["Webhook"])


@router.post("/webhook")
async def webhook(update: Update) -> None:
    """Webhook для обработки обновлений в TelegramBot"""
    await dp.feed_update(bot, update)
    return {"status": "ok"}
