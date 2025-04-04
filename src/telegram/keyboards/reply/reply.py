from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from config import settings


def car_info_confirm(tg_user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✅ Всё верно"),
                KeyboardButton(text="❌ Не верно")
            ],
            [KeyboardButton(text="GearGame 🎮", web_app=WebAppInfo(url=f"{settings.GEAR_URL}/game/{tg_user_id}"))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_problem_keyboard(tg_user_id: int) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🛞 Запчасти"),
                KeyboardButton(text="📿 Аксессуары")
            ],
            [KeyboardButton(text="🛢 Жидкости для авто")],
            [KeyboardButton(text="GearGame 🎮", web_app=WebAppInfo(url=f"{settings.GEAR_URL}/game/{tg_user_id}"))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
