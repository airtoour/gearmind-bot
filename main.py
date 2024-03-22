import asyncio
import uvicorn
from threading import Thread

from src.telegram.bot import dp
from src.db.config import app
from get_env import get_env

async def start_bot():
    await dp.start_polling()

def start_fastapi():
    uvicorn.run(app,
                host=get_env("FASTAPI_HOST"),
                port=int(get_env("FASTAPI_PORT")))


if __name__ == '__main__':
    bot_thread = Thread(target=start_bot)
    fastapi_thread = Thread(target=start_fastapi)

    bot_thread.start()
    fastapi_thread.start()

    bot_thread.join()
    fastapi_thread.join()

