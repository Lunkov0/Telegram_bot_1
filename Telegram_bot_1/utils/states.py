from aiogram.fsm.state import StatesGroup, State


class ChangesOfSchedule(StatesGroup):
    intersection = State()

