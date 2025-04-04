from enum import StrEnum
from typing import Dict, List

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)

from config import settings
from db.models import Cars
from db.models.users.schemas import UsersRoles

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
    ALL_CARS = "https://m3-spb.ru/cars"


# Клавиатура регистрации пользователя
to_signup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Регистрация ✍️", callback_data="signup")]
])

# Клавиатура регистрации Автомобиля пользователя
to_car_register = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Зарегистрировать машину 🚗", callback_data="car")]
])

# Клавиатура возврата в начало процесса регистрации Автомобиля пользователя
retry_register_car = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Начать заново 🔄", callback_data="retry_register_car")]
])

# Клавиатура с переходами на другие ресурсы GearMind
social_links = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Телеграм-канал 🩵", url=UrlsEnum.TG),
        InlineKeyboardButton(text="Instagram* 💜", url=UrlsEnum.IG)
    ]
])

# Клавиатура перехода на сайт с автомобилями
car_list = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Найти мой автомобиль в списке 🔍", web_app=WebAppInfo(url=UrlsEnum.ALL_CARS))]
])

async def car_info(car: Cars) -> InlineKeyboardMarkup:
    keyboard: List = []

    for field, description in CAR_MODULES_MAPPING.values():
        value = getattr(car, field)

        keyboard.append(
            [InlineKeyboardButton(text=f"{description} — {value}", callback_data=f"info:{field}:{value}")]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Клавиатура, запускающая процесс подбора продукции
lets_solution = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Решать проблему 👊", callback_data="solution")]
])

# Клавиатура оценок результата
score_result = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="1 ⭐️", callback_data=f"score:1"),
        InlineKeyboardButton(text="2 ⭐️", callback_data=f"score:2"),
        InlineKeyboardButton(text="3 ⭐️", callback_data=f"score:3"),
        InlineKeyboardButton(text="4 ⭐️", callback_data=f"score:4"),
        InlineKeyboardButton(text="5 ⭐️", callback_data=f"score:5"),
    ]
])

def profile_keyboard(role: UsersRoles) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Редактировать профиль ✍️", callback_data="edit_profile")]
    ]

    if role == UsersRoles.ADMIN:
        keyboard.append([InlineKeyboardButton(text="Админка 🧙‍♀️", url=f"{settings.GEAR_URL}/admin/{role}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)