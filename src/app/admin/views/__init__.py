from typing import List
from sqladmin import ModelView

from .base import AdminBaseView

from .prompts import PromptsView
from .requests import RequestsView
from .users import UsersView
from .scores import ScoresView


views_list: List[ModelView] = [
    AdminBaseView,
    PromptsView,
    RequestsView,
    ScoresView,
    UsersView,
]