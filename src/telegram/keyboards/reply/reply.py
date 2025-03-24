from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def car_info_confirm() -> ReplyKeyboardMarkup:
    """Подтверждение правильности информации о машине"""
    kb = [
        [
            KeyboardButton(text="✅ Всё верно"),
            KeyboardButton(text="❌ Не верно")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard



get_problem_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛞 Запчасти"),
            KeyboardButton(text="📿 Аксессуары")
        ],
        [KeyboardButton(text="🛢 Жидкости для авто")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
