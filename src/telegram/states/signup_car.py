from aiogram.fsm.state import StatesGroup, State


class SignupUserCarStates(StatesGroup):
    car_brand = State()
    car_model = State()
    car_gen = State()
    car_year = State()

    set_result = State()