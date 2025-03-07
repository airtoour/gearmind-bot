from aiogram.fsm.state import StatesGroup, State


class UpdateCarInfo(StatesGroup):
    confirm_info = State()
    correct_part = State()
