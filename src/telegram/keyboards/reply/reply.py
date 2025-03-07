from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def car_info_confirm() -> ReplyKeyboardMarkup:
    """Подтверждение правильности информации о машине"""
    kb = [
        [
            KeyboardButton(text="Всё верно"),
            KeyboardButton(text="Не верно")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


# Отправка контакта пользователя
get_phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Отправить номер телефона ☎️",
                request_contact=True
            )
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Отправьте, пожалуйста, Ваш номер телефона"
)
