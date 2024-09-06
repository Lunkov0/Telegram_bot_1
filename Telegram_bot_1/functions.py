import re
import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram import types

from database.database import dataBase


def list_to_keyboard(items: list[str], columns=2) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    [
        builder.add(types.InlineKeyboardButton(
            text=item,
            callback_data=item,
            ))
        for item in items
    ]
    builder.adjust(columns)  # Кол-во столбцов

    return builder.as_markup(resize_keyboard=False)


def validate_time(time_str):
    '''pattern == 0:00 - 23:59'''
    pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    if re.match(pattern, time_str.strip()):
        return True
    else:
        return False


def validate_phone_number(number):
    digits = ''.join(digit for digit in number if digit.isdigit())

    if len(digits) != 11:
        return False
    return '8' + digits[1:]


def str_to_date(str_date):
    return datetime.datetime.strptime(str_date, '%Y-%m-%d').date()


def date_to_str(date):
    return date.strftime('%Y-%m-%d')


def time_to_str(time):
    return time.strftime('%H:%M')


def str_to_time(time):
    return datetime.datetime.strptime(time, '%H:%M')


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


def appointment_time():
    '''Возвращает итоговое расписание на месяц (пересечения основного расписания и изменений в нём)'''
    # Достанем постоянный перерыв
    constant_breaks = dataBase.get_constant_breaks()
    start_time_constant_breaks, end_time_constant_breaks = constant_breaks[0]

    # Достанем основное расписание для каждого дня недели в формате {3: [[datetime.time(13), datetime.time(2)], ...]}
    schedule = dataBase.schedule_get()
    main_schedule = {}
    for id, day_of_the_week, start_time, end_time in schedule:
        if start_time >= end_time:
            main_schedule[day_of_the_week] = None
        else:
            main_schedule[day_of_the_week] = [[start_time, end_time]]

        # Добавим постоянные перерывы
            if start_time <= start_time_constant_breaks and end_time >= end_time_constant_breaks:
                a = end_time
                main_schedule[day_of_the_week][0][1] = start_time_constant_breaks
                main_schedule[day_of_the_week].append([end_time_constant_breaks, a])
            elif start_time >= start_time_constant_breaks and end_time <= end_time_constant_breaks:
                pass
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


def treatment_schedule(treatment_name):
    schedule = appointment_time()
    duration = dataBase.get_treatment_duration(treatment_name)[0]
    duration = datetime.timedelta(hours=duration.hour, minutes=duration.minute)
    res = {}

    if not schedule:
        return None

    for day, schedule in schedule.items():
        if not schedule:
            res[day] = None
        else:
            for time in schedule:
                start_time = time[0]
                end_time = time[1]

                start_time = datetime.timedelta(hours=start_time.hour, minutes=start_time.minute)
                end_time = datetime.timedelta(hours=end_time.hour, minutes=end_time.minute)

                res[day] = []
                while start_time < end_time:
                    res[day].append(str(start_time)[:-3])

                    start_time += duration
                if not res[day]:
                    res[day] = None

    return res
