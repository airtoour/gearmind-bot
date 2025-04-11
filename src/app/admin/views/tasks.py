from sqladmin import ModelView
from db.models import Tasks


class TasksView(ModelView, model=Tasks):
    name = "Задание мини-игры"
    name_plural = "Задания мини-игры"

    icon = "fa-solid fa-list"

    column_exclude_list = [
        Tasks.id,
        Tasks.user_tasks
    ]
    column_details_exclude_list = [
        Tasks.id,
        Tasks.user_tasks
    ]

    column_labels = {
        Tasks.title: "Название",
        Tasks.description: "Описание",
        Tasks.type: "Тип",
        Tasks.target_value: "Целевое значение",
        Tasks.reward_xp: "Приз за выполнение",
        Tasks.is_active: "Статус"
    }

    column_formatters = {Tasks.type: lambda m, a: m.type.value}
    column_formatters_detail = {Tasks.type: lambda m, a: m.type.value}

    column_searchable_list = [Tasks.type]
