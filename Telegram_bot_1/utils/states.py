from aiogram.fsm.state import StatesGroup, State


class ChangeFSM(StatesGroup):
    date = State()
    intersection = State()
