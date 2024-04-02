from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from flask import url_for

from get_env import get_env


def signup_tap_link() -> InlineKeyboardMarkup:
    url = f'https://{get_env("FASTAPI_HOST")}:{get_env("FASTAPI_PORT")}/{url_for("signup.signup")}'
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Регистрация', web_app=WebAppInfo(url=url))]
    ])
    return markup