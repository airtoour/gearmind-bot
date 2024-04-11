from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from get_env import get_env


def signup_tap_link() -> InlineKeyboardMarkup:
    url = f'https://{get_env("FLASK_HOST")}:{get_env("FLASK_PORT")}/signup/'

    registration = InlineKeyboardButton(text='Регистрация', web_app=WebAppInfo(url=url))
    markup = InlineKeyboardMarkup(inline_keyboard=[[registration],])

    return markup


def order_tap_link() -> InlineKeyboardMarkup:
    url = f'https://{get_env("FLASK_HOST")}:{get_env("FLASK_PORT")}/'

    lets_order = InlineKeyboardButton(text='Перейти', web_app=WebAppInfo(url=url))
    markup = InlineKeyboardMarkup(inline_keyboard=[[lets_order],])

    return markup