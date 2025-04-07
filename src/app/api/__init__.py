from .auth.router import router as auth_router
from .game.router import router as game_router

from .webhook import router as webhook_router


api_routers_list = [
    webhook_router,
    auth_router,
    game_router,
]
