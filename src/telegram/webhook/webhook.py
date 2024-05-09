from src.routes_fastapi.run_fastapi import app
from aiogram import Dispatcher, Bot
from aiogram.types import Update

from src.telegram.bot import bot, dp
from config import config


@app.on_event("startup")
async def on_startup():
    ...

@app.post("")
async def what():
    ...