from typing import List
from aiogram import Router

from .start.start import router as start_router
from .profile import router as profile_router

from .car.register import router as register_cars
from .solution import router as solution_router

from .social import router as social_router
from .help import router as help_router


routers_list: List[Router] = [
    start_router,
    profile_router,
    register_cars,
    solution_router,
    social_router,
    help_router
]
