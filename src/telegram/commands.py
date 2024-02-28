from aiogram.filters import CommandStart
from aiogram.types import Message

from bot import bot, dp

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет, тебя приветствует команда AUTOCOMP.\n'
                         'Если ты к нам обратился, значит с твоей машиной что-то не так :(\n'
                         'Это грустно. Поэтому давай сначала познакомомимся, а потом будем подбирать тебе компоненты.')