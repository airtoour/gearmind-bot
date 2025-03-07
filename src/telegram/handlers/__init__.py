from .start.start import router as start
from .start.signup import router as signup

from .car.register import router as register_cars
from .car.fix_info import router as fix_info_cars
from .solution import router as solution_router

from .social import router as social_router
from .help import router as help_router


routers_list = [
    start,
    signup,
    register_cars,
    fix_info_cars,
    solution_router,
    social_router,
    help_router
]
