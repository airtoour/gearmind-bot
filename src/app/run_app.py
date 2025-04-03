from fastapi import FastAPI
from sqladmin import Admin

from api import routers_list
from admin.views import views_list
from db.db_config import async_engine



app = FastAPI(
    version="1.0",
    title="Assemble Your Car"
)

for router in routers_list:
    app.include_router(router)

admin = Admin(app, async_engine)

for view in views_list:
    admin.add_view(view)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
