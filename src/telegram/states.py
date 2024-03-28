from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    confirm_signup = State()
    menu           = State()


class MenuStates(UserStates):
    order       = State()
    check       = State()
    description = State()
    social      = State()
    faq         = State()
    support     = State()