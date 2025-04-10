from enum import StrEnum
from typing import Dict, List

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.models import Cars
from db.models.users.schemas import UsersRoles

from config import settings

# Маппинг с информацией и названием модулей Автомобиля
CAR_MODULES_MAPPING: Dict[str, str] = {
    "brand_name": "Марка",
    "model_name": "Модель",
    "gen_name": "Комплектация",
    "year": "Год выпуска",
    "mileage": "Пробег"
}

class UrlsEnum(StrEnum):
    """Енам с ссылками на важные ресурсы"""
    TG = "https://t.me/gearmind_team/"
    IG = "https://www.instagram.com/gearmind_team/"


# Клавиатура регистрации пользователя
to_signup = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Регистрация ✍️", callback_data="signup")]
])

# Клавиатура регистрации Автомобиля пользователя
to_car_register = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Зарегистрировать машину 🚗", callback_data="car")]
])

# Клавиатура возврата в начало процесса регистрации Автомобиля пользователя
retry_register_car = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Начать заново 🔄", callback_data="retry_register_car")]
])

# Клавиатура с переходами на другие ресурсы GearMind
social_links = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(text="Телеграм-канал 🩵", url=UrlsEnum.TG),
        types.InlineKeyboardButton(text="Instagram* 💜", url=UrlsEnum.IG)
    ]
])

# Клавиатура перехода на сайт с автомобилями
car_list = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(
            text="Найти мой автомобиль в списке 🔍",
            web_app=types.WebAppInfo(url=settings.CARS_URL)
        )
    ]
])

async def car_info(car: Cars) -> types.InlineKeyboardMarkup:
    keyboard: List = []

    for field, description in CAR_MODULES_MAPPING.values():
        value = getattr(car, field)

        keyboard.append(
            [types.InlineKeyboardButton(text=f"{description} — {value}", callback_data=f"info:{field}:{value}")]
        )

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

# Клавиатура, запускающая процесс подбора продукции
lets_solution = types.InlineKeyboardMarkup(inline_keyboard=[
    [types.InlineKeyboardButton(text="Решать проблему 👊", callback_data="solution")]
])

# Клавиатура оценок результата
score_result = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(text="1 ⭐️", callback_data=f"score:1"),
        types.InlineKeyboardButton(text="2 ⭐️", callback_data=f"score:2"),
        types.InlineKeyboardButton(text="3 ⭐️", callback_data=f"score:3"),
        types.InlineKeyboardButton(text="4 ⭐️", callback_data=f"score:4"),
        types.InlineKeyboardButton(text="5 ⭐️", callback_data=f"score:5"),
    ]
])

def profile_keyboard(role: UsersRoles) -> types.InlineKeyboardMarkup:
    keyboard = [
        [types.InlineKeyboardButton(text="Редактировать профиль ✍️", callback_data="edit_profile")],
        [
            types.InlineKeyboardButton(
                text="GearGame 🎮",
                web_app=types.WebAppInfo(url=f"{settings.GEAR_URL}/game")
            )
        ]
    ]

    if role == UsersRoles.ADMIN:
        keyboard.append(
            [
                types.InlineKeyboardButton(
                    text="Админка 🧙‍♀️",
                    url=f"{settings.GEAR_URL}/admin/{role}"
                )
            ]
        )

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def products_ozon_keyboard(data: Dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = []

    for title, url in data.items():
        keyboard.append(
            [InlineKeyboardButton(text=f"{title}", url=f"{url}")]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)