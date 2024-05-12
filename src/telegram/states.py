from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    user_phone = State()
    user_city = State()

    check_order = State()

    car_register = State()