from sqladmin import ModelView
from db.models import Cars


class CarsView(ModelView, model=Cars):
    name = "Автомобиль"
    name_plural = "Автомобили"

    icon = "fa-solid fa-car"

    column_exclude_list = [
        Cars.id,
        Cars.user_id,
        Cars.full,
        Cars.game_progress
    ]

    column_labels = {
        Cars.user: "Владелец(а)",
        Cars.brand_name: "Марка",
        Cars.model_name: "Модель",
        Cars.gen_name: "Комплектация",
        Cars.year: "Год выпуска",
        Cars.mileage: "Пробег",

        Cars.full: "Полное название",
        Cars.game_progress: "Прогресс игрока"
    }

    column_details_exclude_list = [
        Cars.id,
        Cars.user_id,
        Cars.brand_name,
        Cars.model_name,
        Cars.gen_name,
        Cars.year,
        Cars.mileage
    ]

    column_formatters = {Cars.mileage: lambda m, a: f"{m.mileage} тыс. км"}
    column_formatters_detail = {Cars.mileage: lambda m, a: f"{m.mileage} тыс. км"}

    column_searchable_list = [
        Cars.brand_name,
        Cars.model_name,
        Cars.year
    ]

    can_create = False
    can_edit = False
    can_delete = False
