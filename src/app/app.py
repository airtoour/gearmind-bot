from fastapi import FastAPI
from sqladmin import Admin

from api.base import router as base_router
from admin.views import (
    PromptsView,
    RequestsView,
    UsersView,
    ScoresView
)
from db.db_config import async_engine

app = FastAPI(
    version="1.0",
    title="Assemble Your Car"
)

admin = Admin(app, async_engine)

admin.add_view(PromptsView)
admin.add_view(RequestsView)
admin.add_view(UsersView)
admin.add_view(ScoresView)

app.include_router(base_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
