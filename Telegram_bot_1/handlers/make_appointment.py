from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
import datetime
import locale

# from keyboards.kStart import
from database.database import dataBase
from functions import list_to_keyboard, time_to_str, appointment_time, treatment_schedule
from utils.states import MakeAppointmentFSM

# Установка русской локализации для модуля datetime
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)

router = Router()


def str_to_date(str_date):
    return datetime.datetime.strptime(str_date, '%Y-%m-%d').date()


def date_to_str(date):
    return date.strftime('%Y-%m-%d')


def merge_time(main: list[list[datetime]],
               second: list[datetime],
               is_it_working_day: int = 0) -> list[list[datetime]]:
    if not second:
        return main

    res = []
    start2, end2 = second[0], second[1]

    if is_it_working_day == 0:
        for start1, end1 in sorted(main):
            if start1 <= start2 and end1 >= end2:
                res.append([start1, start2])
                res.append([end2, end1])
            elif start1 >= start2 and end1 >= end2:
                res.append([max(start1, end2), end1])
            elif start1 <= start2 and end1 <= end2:
                res.append([start1, min(end1, start2)])

    elif is_it_working_day == 1:
        sec = [second[0], second[1]]
        for start1, end1 in sorted(main):
            if start1 > end2 or end1 < start2:
                res.append([start1, end1])

            elif start1 <= start2 and end1 >= end2:
                res.append([start1, end1])
                start2, end2 = start1, end1
                sec = []

            else:
                start2 = min(start1, start2)
                end2 = max(end1, end2)
                sec = [start2, end2]

        if sec:
            res.append(sec)

    return sorted(res)


def merge_many(main: list[list[datetime]],
               second: list[list[datetime]],
               is_it_working_day: int = 0) -> list[list[datetime]]:
    res = []

    for val in second:
        res.extend(merge_time(main, val, is_it_working_day))

    return res


@router.callback_query(F.data == 'make_an_appointment')
async def make_an_appointment(callback: types.CallbackQuery, state: FSMContext):
    treatments = dataBase.treatments_get_names()
    keyboard = list_to_keyboard([val[1] for val in treatments])
    await state.set_state(MakeAppointmentFSM.treatment)

    await callback.message.answer(text='Выберите процедуру', reply_markup=keyboard)


@router.callback_query(MakeAppointmentFSM.treatment)
async def m_a_treatment(callback: types.CallbackQuery, state: FSMContext):
    treatment = callback.data
    await state.update_data(treatment=treatment)
    txt = 'Вы выбрали процедуру: ' + treatment + '\nТеперь введи время начала'
    await state.set_state(MakeAppointmentFSM.start_time)

    schedule = treatment_schedule()

    await callback.message.answer(text=txt, reply_markup=schedule)


@router.message(MakeAppointmentFSM.start_time)
async def treatment_start_time(message: types.Message, state: FSMContext):
    start_time = message.text
    await state.update_data(start_time=start_time)
    await message.answer(text=start_time)


@router.message(F.text == '333')
@router.callback_query(F.data.startswith('make_an_appointment_'))
async def some(message: types.Message):
    keyboard = list_to_keyboard(['1', '2', '3', '4', '5', '6', '3', '3', '41', '2', '5'], 3)
    await message.answer(text='Some активирован!!!', reply_markup=keyboard)

