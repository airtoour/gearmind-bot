from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import settings


def signup_tap_link() -> InlineKeyboardMarkup:
    url = f'https://{settings.FASTAPI_HOST}:{settings.FASTAPI_PORT}/signup/'

    registration = InlineKeyboardButton(text='Регистрация', web_app=WebAppInfo(url=url))
    markup = InlineKeyboardMarkup(inline_keyboard=[[registration],])

    return markup


def social_links() -> InlineKeyboardMarkup:
    tg_channel_link = 'https://t.me/autocomp_team/'
    instagram_link = 'https://www.instagram.com/autocomp_team/'
    official_link = 'https://s744844.lpmotortest.com/'

    tg_channel = InlineKeyboardButton(text="Телеграм-канал", url=tg_channel_link)
    instagram = InlineKeyboardButton(text="Instagram", url=instagram_link)
    official = InlineKeyboardButton(text="Официальный сайт", web_app=WebAppInfo(url=official_link))

    markup = InlineKeyboardMarkup(inline_keyboard=[[tg_channel], [instagram], [official]])

    return markup


def car_list() -> InlineKeyboardMarkup:
    url = settings.CARS_URL

    button = InlineKeyboardButton(text='Список машин', web_app=WebAppInfo(url=url))
    markup = InlineKeyboardMarkup(inline_keyboard=[[button],])

    return markup