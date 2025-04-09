from app import STATIC_DIR, TEMPLATES_DIR
from app.admin.views import views_list
from app.api import api_routers_list
from app.exceptions.base import GearMindAPIException

from contextlib import asynccontextmanager
from db.db_config import async_engine

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqladmin import Admin
from services.redis_cache.service import cache_service

from telegram.bot import bot, dp
from telegram.handlers import bot_routers_list

from logger import logger
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    try:
        await bot.set_webhook(
            url=settings.get_webhook_url(),
            allowed_updates=dp.resolve_used_update_types()
        )
        logger.info(f"Webhook установлен")

        await cache_service.connect()
        logger.info("Redis инициализирован")

        yield
    except (Exception, KeyboardInterrupt):
        await bot.delete_webhook()
        await cache_service.disconnect()
        logger.info("Webhook и Redis очищены вручную")
    finally:
        await bot.delete_webhook()
        await cache_service.disconnect()
        logger.info("Webhook и Redis очищены")


# Приложение для API
app = FastAPI(
    title="GearMind API",
    lifespan=lifespan
)

# Добавление API-роутеров
for router in api_routers_list:
    app.include_router(router)

# Подключаем роутеры бота
dp.include_routers(*bot_routers_list)

# Подключаем админку
admin = Admin(app, engine=async_engine, base_url=settings.ADMIN_URL, title="GearAdmin")

for view in views_list:
    admin.add_view(view)

# CORS мидлварь
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Глобальный хендлер ошибок
@app.exception_handler(GearMindAPIException)
async def handle_custom_exception(request: Request, exc: GearMindAPIException):
    return templates.TemplateResponse(
        "errors.html",
        {
            "request": request,
            "status_code": exc.status_code,
            "detail": exc.detail or "Что-то пошло не так"
        },
        status_code=exc.status_code,
    )

# Монтируем статику
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


if __name__ == "__main__":
    """Запуск приложения"""
    import uvicorn

    uvicorn.run(
        app=app,
        host="localhost",
        port=8888,
        forwarded_allow_ips="*",
        proxy_headers=True
    )
