from aiogram.filters import CommandStart
from aiogram.types import Message

from bot import bot, dp
from states import UserStates
from src.db.config import session

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет, мы приветствует команда "AUTOCOMP"\n'
                         'Если ты к нам обратился, значит с твоей машиной что-то не так :(\n'
                         'Это грустно. Поэтому давай сначала познакомомимся, а потом будем подбирать тебе компоненты.')