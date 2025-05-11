from typing import List
from sqladmin import ModelView

from .base import AdminBaseView

from .prompts import PromptsView
from .requests import RequestsView
from .tasks import TasksView
from .users import UsersView
from .cars import CarsView
from .scores import ScoresView

from .game_profiles import ProfilesView

views_list: List[ModelView] = [
    AdminBaseView,

    PromptsView,
    RequestsView,
    ScoresView,

    UsersView,
    CarsView,

    ProfilesView,
    TasksView
]