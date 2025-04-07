from app import STATIC_DIR
from app.admin.views import views_list
from app.api import api_routers_list
from app.api.webhook import lifespan

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqladmin import Admin

from telegram.bot import dp
from telegram.handlers import bot_routers_list

from db.db_config import async_engine
from config import settings


# Инициализация приложения
app = FastAPI(
    version="1.0",
    title="Assemble Your Car",
    lifespan=lifespan
)

# Добавление роутеров aiogram
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

# Добавление мидлвари для обработки работы фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтирование статических файлов
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=80)
