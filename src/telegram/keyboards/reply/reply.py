from aiogram import types


# Метод формирования клавиатуры для подтверждения информации об автомобиле
car_info_confirm = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="✅ Всё верно"),
            types.KeyboardButton(text="❌ Не верно")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Клавиатура получения типа запроса для ИИ
get_type_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="🛞 Запчасти"),
            types.KeyboardButton(text="📿 Аксессуары")
        ],
        [types.KeyboardButton(text="🛢 Жидкости для авто")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
