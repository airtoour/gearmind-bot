from aiogram import types


def order_button() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="Заказать"),
            types.KeyboardButton(text="Проверить свой заказ"),
            types.KeyboardButton(text="Помощь")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите необходимый вариант:"
    )
    return keyboard