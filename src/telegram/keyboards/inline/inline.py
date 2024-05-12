from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import config


def signup_tap_link() -> InlineKeyboardMarkup:
    url = f'https://{config.flask.flask_host}:{config.flask.flask_port}/signup/'

    registration = InlineKeyboardButton(text='Регистрация', web_app=WebAppInfo(url=url))
    markup = InlineKeyboardMarkup(inline_keyboard=[[registration],])

    return markup


def social_links() -> InlineKeyboardMarkup:
    tg_channel_link = 'https://t.me/autocomp_team/'
    instagram_link = 'https://www.instagram.com/autocomp_team/'
    official_link = 'https://autocomp.ru'

    tg_channel = InlineKeyboardButton(text="Телеграм-канал", url=tg_channel_link)
    instagram = InlineKeyboardButton(text="Instagram", url=instagram_link)
    official = InlineKeyboardButton(text="Официальный сайт", web_app=WebAppInfo(url=official_link))

    markup = InlineKeyboardMarkup(inline_keyboard=[[tg_channel], [instagram], [official]])

    return markup


def car_list() -> InlineKeyboardMarkup:
    url = config.car_url.path

    button = InlineKeyboardButton(text='Список машин', web_app=WebAppInfo(url=url))
    markup = InlineKeyboardMarkup(inline_keyboard=[[button],])

    return markup