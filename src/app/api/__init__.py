from .base import router as base_router

from .auth.router import router as auth_router
from .game.router import router as game_router


routers_list = [
    base_router,
    auth_router,
    game_router
]
