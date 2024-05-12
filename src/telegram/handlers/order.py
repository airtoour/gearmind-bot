from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.telegram.states import UserStates
from src.telegram.keyboards.reply.reply import order_button
from src.telegram.keyboards.inline.inline import order_tap_link
# from src.db.db_app import app

# from src.models.models import Orders

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


async def first_vote(message: Message):
    markup = order_tap_link()
    await message.answer('Хорошо, давай приступим к заказу.\n'
                         '\n'
                         'Переходи ниже в приложение, оттуда ты сможешь уже продолжить заказ', reply_markup=markup)


async def second_vote(message: Message, state: FSMContext):
    await message.answer('Для того, чтобы проверить твой заказа, я должен знать номер заказа.\n'
                         'Напиши номер своего заказа, чтобы я смог помочь тебе.')
    await state.set_state(UserStates.check_order)

# async def check_order(message: Message, state: FSMContext):
#    try:
#        with app.app_context():
#            await state.update_data(order_id=message.text)
#
#            get_data = await state.get_data()
#            order_id = get_data.get('order_id')
#
#            order_obj = Orders.query.filter_by(order_id=order_id).first()
#
#            if order_obj:
#                await message.answer('Итаккк... Информация по твоему заказу:\n'
#                                     f'Номер заказа: {Orders.order_id}\n'
#                                     f'Дата заказа: {Orders.order_date}\n'
#                                     f'Состав: {Orders.content}\n'
#                                     f'Статус: {Orders.status}\n'
#                                     f'Сумма: {Orders.summ}\n')
#            else:
#                await message.answer('Кажется, ты ещё ничего не заказывал.'
#                                     'Ты сможешь это сделать через команду /order.')
#            await state.clear()
#    except Exception as e:
#        print('CHECK_ORDER', e)

async def third_vote(message: Message):
    await message.answer('Если с твоим заказом что-то не так, ты всегда можешь обратиться за помощью по команде /help.')