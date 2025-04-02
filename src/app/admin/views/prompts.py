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

    can_delete = False
