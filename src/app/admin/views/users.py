from sqladmin import ModelView
from db.models import Users


class UsersView(ModelView, model=Users):
    name = "Пользователь"
    name_plural = "Пользователи"

    icon = "fa-solid fa-user"

    column_exclude_list = [
        Users.id,
        Users.recommendation_score
    ]
    column_details_exclude_list = [
        Users.id,
        Users.recommendation_score
    ]

    column_labels = {
        Users.car: "Автомобиль",
        Users.game_progress: "Прогресс в игре",
        Users.tg_user_id: "TelegramID",
        Users.name: "Имя",
        Users.role: "Роль"
    }

    column_formatters = {Users.role: lambda m, a: m.role.value}
    column_formatters_detail = {Users.role: lambda m, a: m.role.value}

    can_delete = False