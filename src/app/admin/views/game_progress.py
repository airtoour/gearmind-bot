from sqladmin import ModelView
from db.models import GameProgressUsers


class ProgressView(ModelView, model=GameProgressUsers):
    name = "Прогресс GearGame"
    name_plural = "Прогрессы GearGame"

    icon = "fa-solid fa-gears"

    column_exclude_list = [
        GameProgressUsers.id,
        GameProgressUsers.user_id,
        GameProgressUsers.car_id
    ]

    column_details_exclude_list = [
        GameProgressUsers.id,
        GameProgressUsers.user_id,
        GameProgressUsers.car_id
    ]

    can_create = False
    can_edit = False
    can_delete = False
