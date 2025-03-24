from fastapi import FastAPI
from sqladmin import Admin

from api.base import router as base_router

from db.db_config import async_engine

app = FastAPI(
    debug=True,
    version="1.0",
    title="Assemble Your Car"
)

admin = Admin(app, async_engine)

app.include_router(base_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
