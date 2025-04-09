from .game.router import router as game_router
from .cars.router import router as car_router
from .webhook import router as webhook_router
from .users_tasks.router import router as users_tasks_router
from .tasks.router import router as sprav_tasks_router


api_routers_list = [
    webhook_router,

    car_router,

    game_router,
    users_tasks_router,
    sprav_tasks_router
]
