from sqladmin import ModelView
from db.models import UsersGameProfiles


class ProfilesView(ModelView, model=UsersGameProfiles):
    name = "Профиль GearGame"
    name_plural = "Профили GearGame"

    icon = "fa-solid fa-gears"

    column_exclude_list = [
        UsersGameProfiles.id,
        UsersGameProfiles.user_id,
        UsersGameProfiles.car_id
    ]

    column_details_exclude_list = [
        UsersGameProfiles.id,
        UsersGameProfiles.user_id,
        UsersGameProfiles.car_id
    ]

    can_create = False
    can_edit = False
    can_delete = False
