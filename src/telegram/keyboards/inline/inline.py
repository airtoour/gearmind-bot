from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from db.models.users.repository import UsersRepository
from db.models.cars.repository import CarsRepository

from config import settings


to_signup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Регистрация", callback_data="/signup")]
])

to_car_register = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Зарегистрировать машину", callback_data="/car")]
])

social_links = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Телеграм-канал", url="https://t.me/autocomp_team/")],
    [InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/autocomp_team/")]
])


def car_list() -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text="Список машин", web_app=WebAppInfo(url=settings.CARS_URL))
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])

    return markup


def car_info(user_id: int) -> InlineKeyboardMarkup:
    car = CarsRepository.find_one_or_none(user_id=user_id)
    keyboard = []
    fields = ["brand_name", "model_name", "gen_name", "year"]

    for field in fields:
        value = getattr(car, field)
        keyboard.append([
            InlineKeyboardButton(text=str(value), callback_data=f"info:{str(field)}")
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

lets_solution = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Решать проблему", callback_data="/solution")]
])


def prod_types() -> InlineKeyboardMarkup:
    tables = ["Масла", "Шины", "Аккумуляторы", "Диски"]
    keyboard = []

    for i in range(0, len(tables), 2):
        row = [
            InlineKeyboardButton(text=tables[i], callback_data=f"table:{tables[i]}"),
            InlineKeyboardButton(text=tables[i + 1] if i + 1 < len(tables) else "",
                                 callback_data=f"table:{tables[i + 1]}" if i + 1 < len(tables) else "")
        ]
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def first_param(table: str):
    keyboard = []
    if table == "oils":
        comments = ["10W40", "5W40"]
        for comment in comments:
            row = [
                InlineKeyboardButton(text=str(comment), callback_data=str(f"value:{comment}"))
            ]
            keyboard.append(row)
    if table == "busbars":
        diameters = [13, 14, 16, 18]
        for i in range(0, len(diameters), 2):
            row = [
                InlineKeyboardButton(text=str(diameters[i]), callback_data=str(f"value:{diameters[i]}")),
                InlineKeyboardButton(text=str(diameters[i + 1]) if i + 1 < len(diameters) else "",
                                     callback_data=str(f"value:{diameters[i + 1]}") if i + 1 < len(diameters) else "")
            ]
            keyboard.append(row)
    if table == "batteries":
        capacities = [1, 2.1, 2.3, 2.5, 55]
        for i in range(0, len(capacities), 3):
            row = [
                InlineKeyboardButton(text=str(capacities[i]), callback_data=str(f"value:{capacities[i]}")),
                InlineKeyboardButton(text=str(capacities[i + 1]) if i + 1 < len(capacities) else "",
                                     callback_data=str(f"value:{capacities[i + 1]}") if i + 1 < len(capacities) else "")
            ]
            keyboard.append(row)
    if table == "disks":
        diameters = [13, 14, 15, 16, 17]
        for i in range(0, len(diameters), 3):
            row = [
                InlineKeyboardButton(text=str(diameters[i]), callback_data=str(f"value:{diameters[i]}")),
                InlineKeyboardButton(text=str(diameters[i + 1]) if i + 1 < len(diameters) else '',
                                     callback_data=str(f"value:{diameters[i + 1]}") if i + 1 < len(diameters) else "")
            ]
            keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def result_solution(table_name: str, comment: str, user_id: int) -> InlineKeyboardMarkup:
    user = await UsersRepository.get_by_tg(tg_id=user_id)
    car = await CarsRepository.find_one_or_none(user_id=user.id)
    url = (f"https://www.wildberries.ru/catalog/0/search.aspx?search={table_name} {comment} "
           f"Для машины {car.brand_name} {car.model_name} {car.gen_name} {car.year}")
    button = InlineKeyboardButton(text="Посмотреть результат", url=url)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return keyboard
