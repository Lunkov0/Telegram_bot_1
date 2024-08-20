from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import datetime
import locale

# from keyboards.kStart import
from database.database import dataBase
from functions import list_to_keyboard

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


def appointment_time():
    '''Возвращает итоговое расписание на месяц (пересечения основного расписания и изменений в нём)'''
    # Достанем постоянный перерыв
    constant_breaks = dataBase.get_constant_breaks()
    start_time_constant_breaks, end_time_constant_breaks = constant_breaks[0]

    # Достанем основное расписание для каждого дня недели в формате {3: [[datetime.time(13), datetime.time(2)], ...]}
    schedule = dataBase.schedule_get()
    main_schedule = {}
    for id, day_of_the_week, start_time, end_time in schedule:
        main_schedule[day_of_the_week] = [[start_time, end_time]]

        # Добавим постоянные перерывы
        if start_time <= start_time_constant_breaks and end_time >= end_time_constant_breaks:
            a = end_time
            main_schedule[day_of_the_week][0][1] = start_time_constant_breaks
            main_schedule[day_of_the_week].append([end_time_constant_breaks, a])
        elif start_time >= start_time_constant_breaks and end_time <= end_time_constant_breaks:
            main_schedule[day_of_the_week][0][0] = []
        elif start_time >= start_time_constant_breaks and end_time >= end_time_constant_breaks:
            main_schedule[day_of_the_week][0][0] = max(end_time_constant_breaks, start_time)
        elif start_time <= start_time_constant_breaks and end_time <= end_time_constant_breaks:
            main_schedule[day_of_the_week][0][1] = min(end_time, start_time_constant_breaks)

    # Достанем изменения в расписании {datetime.date(2024, 9, 3): [['12:00:00', '14:00:00', 1],
    #                                  ['16:00:00', '22:00:00', 0]...]}
    schedule_changes = dataBase.get_all_schedule_changes()
    changed_schedule = {}
    for id, start_date, end_date, is_it_a_working_day in schedule_changes:
        if changed_schedule.get(start_date.date(), False):
            changed_schedule[start_date.date()].append([start_date.time(), end_date.time(), is_it_a_working_day])
        else:
            changed_schedule[start_date.date()] = [[start_date.time(), end_date.time(), is_it_a_working_day]]

    date_now = datetime.date.today()
    schedule = {}
    # return date_now, changed_schedule

    for i in range(30):
        if not changed_schedule.get(date_now, False):
            schedule[date_now] = main_schedule[date_now.weekday()]

        else:
            main = main_schedule[date_now.weekday()]
            changes = changed_schedule[date_now]

            for start, end, is_it_working_day in changes:
                schedule[date_now] = merge_time(main, [start, end], is_it_working_day)
        date_now += datetime.timedelta(days=1)

    return schedule


@router.callback_query(F.data == 'make_an_appointment')
async def make_an_appointment(callback: types.CallbackQuery):
    treatments = dataBase.treatments_get_names()

    builder = InlineKeyboardBuilder()
    for service_id, service in treatments:
        builder.add(types.InlineKeyboardButton(text=service, callback_data=f'make_an_appointment_{service}'))
    builder.adjust(2)  # Кол-во столбцов

    await callback.message.answer(text='Выберите процедуру', reply_markup=builder.as_markup(resize_keyboard=False))


@router.callback_query(F.data.startswith('make_an_appointment_'))
async def m_a_treatment(callback: types.CallbackQuery):
    treatment = callback.data.split('_')[-1]
    txt = 'Вы выбрали процедуру: ' + treatment

    await callback.message.answer(text=txt)


@router.message(F.text == '333')
@router.callback_query(F.data.startswith('make_an_appointment_'))
async def some(message: types.Message):
    keyboard = list_to_keyboard(['1', '2', '3', '4', '5', '6', '3', '3', '41', '2', '5'], 3)
    await message.answer(text='Some активирован!!!', reply_markup=keyboard)


print(appointment_time())
