from aiogram.types import Message
from src.telegram.keyboards.inline.inline import social_links

async def social(message: Message):
    markup = social_links()
    await message.answer('Хочешь узнать лучше о нас?\n'
                         'Переходи по ссылкам на социальные сети ниже!', reply_markup=markup)