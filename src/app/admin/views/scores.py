from sqladmin import ModelView
from db.models import Scores


class ScoresView(ModelView, model=Scores):
    name = "Оценка запроса"
    name_plural = "Оценки запросов"

    icon = "fa-solid fa-poo"

    column_exclude_list = [
        Scores.id,
        Scores.request_id,
        Scores.user_id
    ]

    column_details_exclude_list = [
        Scores.id,
        Scores.request_id,
        Scores.user_id
    ]

    can_delete = False
    can_edit = False
    can_create = False
