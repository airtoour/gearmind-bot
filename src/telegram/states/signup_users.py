from aiogram.fsm.state import StatesGroup, State


class SignupUserStates(StatesGroup):
    name = State()
