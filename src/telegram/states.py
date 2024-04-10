from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    confirm_signup = State()

    check_order = State()