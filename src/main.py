from app import STATIC_DIR
from app.api import api_routers_list
from app.admin.views import views_list

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqladmin import Admin

from telegram.bot import bot, dp
from telegram.handlers import bot_routers_list

from db.db_config import async_engine

from config import settings
from logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = settings.get_webhook_url()

    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types()
    )
    logger.info(f"Webhook set to {webhook_url}")

    yield

    await bot.delete_webhook()
    logger.info("Webhook removed")


# Определение приложения
app = FastAPI(
    version="1.0",
    title="Assemble Your Car",
    lifespan=lifespan
)

dp.include_routers(*bot_routers_list)

# Подключаем роутеры
for router in api_routers_list:
    app.include_router(router)

# Определяем админку
admin = Admin(
    app,
    engine=async_engine,
    base_url=settings.ADMIN_URL,
    title="GearAdmin"
)

# Подключаем вьюхи для админки
for view in views_list:
    admin.add_view(view)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=80)
