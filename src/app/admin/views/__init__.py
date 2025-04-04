from typing import List
from sqladmin import ModelView

from .base import AdminBaseView

from .prompts import PromptsView
from .requests import RequestsView
from .users import UsersView
from .cars import CarsView
from .scores import ScoresView

from .game_progress import ProgressView

views_list: List[ModelView] = [
    AdminBaseView,
    PromptsView,
    RequestsView,
    ScoresView,
    UsersView,
    CarsView,
    ProgressView,
]