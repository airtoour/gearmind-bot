from aiogram.fsm.state import StatesGroup, State


class SolutionStates(StatesGroup):
    solution_type = State()