from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    registration = State()
    lets_order = State()
