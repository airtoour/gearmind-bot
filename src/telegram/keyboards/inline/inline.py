from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from get_env import get_env


def signup_tap_link(user_id: int) -> InlineKeyboardMarkup:
    from src.db.config import app

    url = f'https://{get_env("FASTAPI_HOST")}:{get_env("FASTAPI_PORT")}{app.url_path_for("signup", user_id=user_id)}'
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Регистрация', web_app=WebAppInfo(url=url))]
    ])
    return markup