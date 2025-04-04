from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from api import routers_list
from admin.views import views_list

from db.db_config import async_engine

from config import settings


# Определение приложения
app = FastAPI(
    version="1.0",
    title="Assemble Your Car"
)

# Подключаем роутеры
for router in routers_list:
    app.include_router(router)

# Определяем админку
admin = Admin(
    app,
    engine=async_engine,
    base_url=f"/admin/Администратор",
    title="GearAdmin"
)

# Подключаем вьюхи для админки
for view in views_list:
    admin.add_view(view)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.GEAR_URL],
    allow_headers=["*"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=80)
