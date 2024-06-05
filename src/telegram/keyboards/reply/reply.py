from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def car_info_confirm() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="Всё верно"),
            KeyboardButton(text="Не верно")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Верна ли информация о твоей машине?",
        one_time_keyboard=True
    )
    return keyboard
