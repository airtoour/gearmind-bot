from httpx import AsyncClient
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

from aiogram.types import Message
from src.db.models.models import Cars

car_info = []


async def get_brand(url: str, msg: str):
    async with AsyncClient() as client:
        response = await client.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    car_links = soup.find('a', title=msg)

    for link in car_links:
        car_name = link.text
        car_info.append(car_name)

    print(car_info)
    return car_info


async def register_car(user_message: str, url: str):
    user_message = user_message.lower().strip()

    get_car_info = await get_brand(url, user_message)

    for car_model in get_car_info:
        similarity = fuzz.ratio(user_message, car_model)

        if similarity > 80:
            print(f"Модель машины {car_model} найдена в сообщении пользователя")
            Cars.car_register(get_car_info[0], get_car_info[1], get_car_info[2], get_car_info[3], Message.text)
        else:
            print(f"Модель машины {car_model} не найдена в сообщении пользователя")