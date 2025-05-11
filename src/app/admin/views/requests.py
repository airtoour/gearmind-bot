from sqladmin import ModelView

from db.models import Requests


class RequestsView(ModelView, model=Requests):
    name = "Запрос к ИИ"
    name_plural = "Запросы к ИИ"

    icon = "fa-solid fa-comments"

    column_exclude_list = [
        Requests.id,
        Requests.score,
        Requests.prompt_id
    ]

    column_details_exclude_list = [
        Requests.id,
        Requests.score,
        Requests.prompt_id
    ]

    can_delete = False
    can_edit = False
    can_create = False
