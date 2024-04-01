from aiogram.types import Message
from aiogram.fsm.context import FSMContext


async def order(message: Message, state: FSMContext):
    try:
        pass
    except Exception as e:
        print('order: ', e)