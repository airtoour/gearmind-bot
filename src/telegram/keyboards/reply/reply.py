from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


car_info_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Всё верно"),
            KeyboardButton(text="❌ Не верно")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


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
