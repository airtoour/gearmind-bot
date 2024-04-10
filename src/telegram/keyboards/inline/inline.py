from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from get_env import get_env


def signup_tap_link() -> InlineKeyboardMarkup:
    url = f'https://{get_env("FLASK_HOST")}:{get_env("FLASK_PORT")}/signup/'
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Регистрация', web_app=WebAppInfo(url=url))
        ],
    ])
    return markup


def order_tap_link() -> InlineKeyboardMarkup:
    url = f'https://{get_env("FLASK_HOST")}:{get_env("FLASK_PORT")}/letsorder/'
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
           InlineKeyboardButton(text='Перейти', web_app=WebAppInfo(url=url))
        ],
    ])
    return markup