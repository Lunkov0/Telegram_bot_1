from aiogram.fsm.state import StatesGroup, State


class ChangeFSM(StatesGroup):
    date = State()
    hour_start = State()
    intersection = State()
    add_treatments = State()


class TreatmentFSM(StatesGroup):
    name = State()
    duration = State()
    price = State()
    description = State()
    final = State()


class ConstantBreaksFSM(StatesGroup):
    start_time = State()
    end_time = State()


class MakeAppointmentFSM(StatesGroup):
    treatment = State()
    schedule = State()
    end_time = State()
