from .auth.router import router as auth_router
from .game.router import router as game_router


routers_list = [
    auth_router,
    game_router
]
