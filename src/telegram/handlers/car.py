from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.telegram.filters.get_car import register_car
from src.telegram.states import UserStates
from src.models.users import Users
from src.telegram.keyboards.inline.inline import car_list

from config import settings

async def car(message: Message, state: FSMContext):
    try:
        user = Users.get_current(message.from_user.id)

        if user:
            link = car_list()

            await message.answer(
                "Для регистрации машины напиши, пожалуйста, модель своей машины в виде:\n"
                "'Lada, Priora Седан, 2012 года, модификация ВАЗ-21114'.\n"
                "\n"
                "Я зарегистрирую твою машину в нашей базе данных, а далее исходя из модели твоей машины"
                "мы сможем искать и подбирать тебе запчасти и прочее, в зависимости от твоих потребностей\n"
                "Если ты не знаешь точных данных своей машины, ты можешь посмотреть точные данные по ссылке ниже\n"
                "\n"
                "P.S. Рекомендуется проверить точные данные о Вашей машине, "
                "т.к. данные вносятся в соответствии с данными сайта.",
                reply_markup=link
            )
            await state.set_state(UserStates.car_register)
        else:
            await message.answer(
                "Сначала требуется пройти регистрацию, только потом ты сможешь зарегистрировать свою машину.\n"
                "Пройти регистрацию ты можешь по команде /start. Удачи <3"
            )
    except Exception as e:
        await message.answer('Кажется, произошла какая-то ошибка.\n'
                             'Стараемся разобраться с этим, извините за неудобства...')
        print('car', e)

async def register(message: Message, state: FSMContext):
    try:
        await state.update_data(model=message.text)

        get_data = await state.get_data()
        model = get_data.get('model')

        await register_car(model, settings.CARS_URL)

        await message.answer("Отлично, твоя машина зарегистрирована у нас! ")
    except Exception as e:
        await message.answer('Кажется, произошла какая-то ошибка.\n'
                             'Стараемся разобраться с этим, извините за неудобства...')
        print('register', e)