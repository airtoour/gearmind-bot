from sqladmin import ModelView
from db.models import Prompts


class PromptsView(ModelView, model=Prompts):
    name = "Промпт"
    name_plural = "Промпты"

    icon = "fa-solid fa-wand-magic-sparkles"

    column_exclude_list = [
        Prompts.id,
        Prompts.requests
    ]
    column_details_exclude_list = [
        Prompts.id,
        Prompts.requests
    ]

    column_labels = {
        Prompts.type: "Тип",
        Prompts.text: "Текст"
    }

    column_formatters = {Prompts.type: lambda m, a: m.type.value}
    column_formatters_detail = {Prompts.type: lambda m, a: m.type.value}

    column_searchable_list = [Prompts.type]

    can_delete = False
