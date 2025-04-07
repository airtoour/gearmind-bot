from typing import Optional
from aiogram import types
from config import settings


def car_info_confirm(tg_user_id: Optional[int] = None) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="✅ Всё верно"),
                types.KeyboardButton(text="❌ Не верно")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_problem_keyboard(tg_user_id: Optional[int] = None) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="🛞 Запчасти"),
                types.KeyboardButton(text="📿 Аксессуары")
            ],
            [types.KeyboardButton(text="🛢 Жидкости для авто")],
            [
                types.KeyboardButton(
                    text="GearGame 🎮",
                    web_app=types.WebAppInfo(url=f"{settings.GEAR_URL}/")
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
