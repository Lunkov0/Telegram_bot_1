from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import datetime
import locale

# from keyboards.kStart import
from database.database import dataBase


# Установка русской локализации для модуля datetime
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)


router = Router()


def appointment_time():
    '''Возвращает итоговое расписание на месяц (пересечения основного расписания и изменений в нём)'''
    # Достанем постоянный перерыв
    constant_breaks = dataBase.get_constant_breaks()
    start_time_constant_breaks, end_time_constant_breaks = constant_breaks[0]

    # Достанем основное расписание для каждого дня недели в формате {3: [['12:00:00', '22:00:00'], ...]}
    schedule = dataBase.schedule_get()
    main_schedule = {}
    for id, day_of_the_week, start_time, end_time in schedule:
        main_schedule[day_of_the_week] = [[start_time, end_time]]

        # Добавим постоянные перерывы
        if start_time <= start_time_constant_breaks and end_time >= end_time_constant_breaks:
            a = end_time
            main_schedule[day_of_the_week][0][1] = start_time_constant_breaks
            main_schedule[day_of_the_week][0].append([end_time_constant_breaks, a])
        elif start_time >= start_time_constant_breaks and end_time <= end_time_constant_breaks:
            main_schedule[day_of_the_week][0][0] = []
        elif start_time >= start_time_constant_breaks and end_time >= end_time_constant_breaks:
            main_schedule[day_of_the_week][0][0] = max(end_time_constant_breaks, start_time)
        elif start_time <= start_time_constant_breaks and end_time <= end_time_constant_breaks:
            main_schedule[day_of_the_week][0][1] = min(end_time, start_time_constant_breaks)
    return main_schedule

    # Достанем изменения в расписании {'2034-12-29': [['12:00:00', '14:00:00'], ['16:00:00', '22:00:00']...]}
    schedule_changes = dataBase.get_all_schedule_changes()
    changed_schedule = {}
    for id, start_date, end_date, is_it_a_working_day in schedule_changes:
        if changed_schedule.get(start_date.date(), False):
            changed_schedule[start_date.date()].append([start_date, end_date, is_it_a_working_day])
        else:
            changed_schedule[start_date.date()] = [[start_date, end_date, is_it_a_working_day]]

    # Сгенерируем расписание для следующих 30 дней
    date_now = datetime.date.today()
    schedule = {}
    for i in range(30):
        date = date_now + datetime.timedelta(days=i)
        hours = date.weekday()
        # schedule[date] =


    # Возвращаем Словарь из 30-ти дней - {'2034-12-29': [['12:00:00', '14:00:00'], ['16:00:00', '22:00:00']...]}
    return schedule


@router.callback_query(F.data == 'make_an_appointment')
async def make_an_appointment(callback: types.CallbackQuery):
    treatments = dataBase.treatments_get_names()

    builder = InlineKeyboardBuilder()
    for service_id, service in treatments:
        builder.add(types.InlineKeyboardButton(text=service, callback_data=f'make_an_appointment_{service_id}'))
    builder.adjust(2)  # Кол-во столбцов

    await callback.message.answer(text='Выберите процедуру', reply_markup=builder.as_markup(resize_keyboard=False))


@router.callback_query(F.data.startswith('make_an_appointment_'))
async def m_a_treatment(callback: types.CallbackQuery):
    treatment = callback.data.split('_')[-1]
    txt = 'Вы выбрали процедуру'
    txt1 = dataBase.schedule_get()
    txt2 = dataBase.get_all_schedule_changes()
    txt3 = txt + txt1 + str(txt2)
    await callback.message.answer(text=txt3)

@router.message(F.text == '1')
async def somee(message: types.Message):
    txt = str(appointment_time())
    await message.answer(text=txt)


x = dataBase.get_all_schedule_changes()
# print(constant_breaks[0])
print(x)
