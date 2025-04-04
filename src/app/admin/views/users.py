from sqladmin import ModelView
from db.models import Users


class UsersView(ModelView, model=Users):
    name = "Пользователь"
    name_plural = "Пользователи"

    icon = "fa-solid fa-user"

    column_exclude_list = [
        Users.id,
        Users.car,
        Users.recommendation_score
    ]
    column_details_exclude_list = [
        Users.id,
        Users.car,
        Users.recommendation_score
    ]

    can_delete = False