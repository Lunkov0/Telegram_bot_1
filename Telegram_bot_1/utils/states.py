from aiogram.fsm.state import StatesGroup, State


class ChangeFSM(StatesGroup):
    date = State()
    hour_start = State()
    intersection = State()
