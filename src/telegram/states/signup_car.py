from aiogram.fsm.state import StatesGroup, State


class SignupUserCarStates(StatesGroup):
    brand = State()
    model = State()
    gen = State()
    year = State()
    mileage = State()
