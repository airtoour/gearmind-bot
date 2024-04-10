from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

from src.telegram.keyboards.reply.reply import order_button
from src.telegram.keyboards.inline.inline import order_tap_link
from src.telegram.bot import dp

from src.models.models import Orders
from src.telegram.states import UserStates

async def order(message: Message):
    try:
        markup = order_button()
        await message.answer('Это панель с заказами!\n'
                             'Тут ты сможешь по кнопке ниже перейти в приложение и заказать всё тебе необходимое.\n'
                             'Также можешь проверить статус своего заказа, если он есть\n'
                             'Также если тебе необходима помощь, выбери "Помощь".\n'
                             '\n'
                             'А теперь, выбери то, что тебе нужно ниже..', reply_markup=markup)
    except Exception as e:
        print('order: ', e)


@dp.message(F.text.lower() == "заказать")
async def first_vote(message: Message):
    markup = order_tap_link()
    await message.answer('Хорошо, давай приступим к заказу.\n'
                         '\n'
                         'Переходи ниже в приложение, оттуда ты сможешь уже продолжить заказ <3', reply_markup=markup)


@dp.message(F.text.lower() == "проверить свой заказ")
async def second_vote(message: Message, state: FSMContext):
    await message.answer('Для того, чтобы проверить статус твоего заказа, я должен знать номер заказа.\n'
                         'Напиши номер своего заказа, чтобы я смог помочь тебе.')
    await state.set_state(UserStates.check_order)

@dp.message(StateFilter(UserStates.check_order))
async def check_order(message: Message, state: FSMContext):
    await state.update_data(order_id=message.text)

    get_data = await state.get_data()
    order_id = get_data.get('order_id')

    order_obj = Orders.query.filter_by(order_id=order_id).first()

    if order_obj:
        await message.answer('Итаккк..., информация по твоему заказу:\n'
                             f'Номер заказа: {Orders.order_id}\n'
                             f'Состав заказа №{Orders.order_id}: \n'
                             f'Статус заказа №{Orders.order_id}: \n'
                             f'Сумма заказа №{Orders.order_id}: ')