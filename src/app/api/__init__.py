from .game.router import router as game_router
from .cars.router import router as car_router
from .webhook import router as webhook_router


api_routers_list = [
    webhook_router,
    game_router,
    car_router
]
