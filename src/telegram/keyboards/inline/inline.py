from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import config


def signup_tap_link() -> InlineKeyboardMarkup:
    url = f'https://{config.flask.flask_host}:{config.flask.flask_port}/signup/'

    registration = InlineKeyboardButton(text='Регистрация', web_app=WebAppInfo(url=url))
    markup = InlineKeyboardMarkup(inline_keyboard=[[registration],])

    return markup


def order_tap_link() -> InlineKeyboardMarkup:
    url = f'https://{config.flask.flask_host}:{config.flask.flask_port}/'

    lets_order = InlineKeyboardButton(text='Перейти', web_app=WebAppInfo(url=url))
    markup = InlineKeyboardMarkup(inline_keyboard=[[lets_order],])

    return markup