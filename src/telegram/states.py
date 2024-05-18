from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    phone = State()

    confirm_info = State()
    correct_part = State()

    car_brand = State()
    car_model = State()
    car_gen = State()
    car_year = State()

    set_result = State()