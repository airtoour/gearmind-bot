from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def order_button() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Заказать"),
            KeyboardButton(text="Проверить свой заказ"),
            KeyboardButton(text="Помощь")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите необходимый вариант:",
        one_time_keyboard=True
    )
    return keyboard