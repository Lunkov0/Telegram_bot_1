from pydoc import html

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm import state

import datetime

import constants
from database.database import dataBase
from keyboards.kAdmin import kb_admin, kb_admin_schedule, kb_c_s_type
from database.database import dataBase
from constants import WEEKDAY
from utils.states import ChangeFSM

router = Router()


@router.message(F.text.lower() == '123')
async def admin_p(message: Message):
    await message.answer(
        'Это админ панель.\n\nЗдесь ты можешь настроить стандартное расписание (для каждого дня недели выставляется график работы)\n\nИсключения для рассписания (на конкретную дату добавляется дополнительное рабочее время или наоборот убирается)',
        reply_markup=kb_admin,
    )


# Пишет текущее расписание. Выдает дни недели для смены расписания.
@router.callback_query(F.data == 'schedule')
async def schedule(callback: types.CallbackQuery):
    s = dataBase.schedule_get()
    weekday = [i for i in range(7)]
    for i, num, start, stop in s:
        weekday[int(num)] = f'{constants.WEEKDAY[int(num)]}: с {str(start)[:5]} до {str(stop)[:5]}'

    builder = InlineKeyboardBuilder()
    for num, day in constants.WEEKDAY.items():
        builder.add(types.InlineKeyboardButton(text=day, callback_data=f'schedule_set_{num}'))
    builder.adjust(2)  # Кол-во столбцов)

    txt = 'Твоё текущее расписание:\n\n' + '\n'.join(weekday) + '\n\n Кнопками ниже можно изменить часы работы'
    await callback.message.answer(text=txt, reply_markup=builder.as_markup(resize_keyboard=False))


# Меняем время начала работы стандартного расписания
@router.callback_query(F.data.startswith('schedule_set_'))
async def schedule_set(callback: types.CallbackQuery):
    # Достанем название дня недели
    weekday_num = callback.data.split('_')[-1]
    weekday = WEEKDAY[int(weekday_num)]

    builder = InlineKeyboardBuilder()
    for hour in range(5, 24):
        s_hour = f'{hour}:00'
        builder.add(types.InlineKeyboardButton(text=s_hour, callback_data=f'schedule_start_set_{weekday_num}_{s_hour}'))
    builder.adjust((3))

    txt = f'Далее установим начало работы в {weekday}'
    await callback.message.answer(text=txt, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('schedule_start_set_'))
async def schedule_set_s(callback: types.CallbackQuery):
    hour = callback.data.split('_')[-1]
    weekday = callback.data.split('_')[-2]
    dataBase.schedule_set_s(hour, weekday)

    builder = InlineKeyboardBuilder()
    for h in range(5, 24):
        s_hour = f'{h}:00'
        builder.add(types.InlineKeyboardButton(text=s_hour, callback_data=f'schedule_finish_set_{weekday}_{s_hour}'))
    builder.adjust((3))

    txt = f'Теперь установим время конца работы'
    await callback.message.answer(text=txt, reply_markup=builder.as_markup())


# Меняем время конца работы стандартного расписания
@router.callback_query(F.data.startswith('schedule_finish_set_'))
async def schedule_set_f(callback: types.CallbackQuery):
    hour = callback.data.split('_')[-1]
    weekday = callback.data.split('_')[-2]
    dataBase.schedule_set_f(hour, weekday)

    txt = 'Отлично! Стандартное время работы обновлено!\n\nОбновить еще один день недели?'
    await callback.message.answer(text=txt, reply_markup=kb_admin)


'''************************* schedule of changes ******************************'''
@router.callback_query(F.data == 'change_of_schedule')
async def change_of_schedule(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    for next_day in range(30):
        # текущая день плюс число из счетчика 'next_day'
        day = datetime.date.today() + datetime.timedelta(days=next_day)
        builder.add(types.InlineKeyboardButton(text=str(day), callback_data=f'c_s_days_{str(day)}'))
    builder.adjust((3))

    txt = 'Расписание на какую дату поменяем?'
    # await state.set_state(ChangeFSM.date)
    await callback.message.answer(text=txt, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('c_s_days_'))
async def c_s_days(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    date = data[-1]
    await state.update_data(date=date)

    builder = InlineKeyboardBuilder()
    for h in range(5, 24):
        s_hour = f'{h}:00'
        builder.add(types.InlineKeyboardButton(text=s_hour, callback_data=f'c_s_hours_start_{s_hour}'))
    builder.adjust((3))

    await state.set_state(ChangeFSM.intersection)
    await callback.message.answer(text='Напиши, со скольки ты будешь работать в эту дату?',
                                  reply_markup=builder.as_markup())


# @router.message(ChangeFSM.intersection)
@router.callback_query(F.data.startswith('c_s_hours_start_'))
async def c_s_time(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    hour_start = data[-1]
    await state.update_data(hour_start=hour_start)

    # Достаем данные из машины состояний
    # data = await state.get_data()
    # days = data.get('date')
    # hour_start = data.get('hour_start')
    # await callback.message.answer(days)
    # await callback.message.answer(hour_start)

    builder = InlineKeyboardBuilder()
    for h in range(5, 24):
        s_hour = f'{h}:00'
        builder.add(types.InlineKeyboardButton(text=s_hour, callback_data=f'c_s_hours_end_{s_hour}'))
    builder.adjust((3))

    # await state.set_state(ChangeFSM.intersection)
    await callback.message.answer(text=f'Начинаешь в {hour_start}, а во сколько планируешь закончить свой рабочий день?',
                                  reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('c_s_hours_end_'))
async def c_s_type(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    hour_end = data[-1]
    await state.update_data(hour_end=hour_end)

    data = await state.get_data()

    start_date = f'{data['date']} {data['hour_start']}'
    end_date = f'{data['date']} {data['hour_end']}'

    await state.update_data(start_date=start_date)
    await state.update_data(end_date=end_date)

    # Get the data already recorded for this day
    intersection = dataBase.get_schedule_changes(data['date'])
    if not intersection:
        intersection_text = ''
    else:
        is_it_working_time = {0: 'Время отдыха', 1: 'Рабочее время'}
        intersection_text = 'Я вижу, что в этот день уже есть изменения:\n'
        for time in intersection:
            intersection_text += f'С {time[1].hour} до {time[2].hour}. {is_it_working_time[int(time[3])]} \n'

    txt = f'Выбрана дата {data['date']} c {data['hour_start']} по {data['hour_end']}.\n\n{intersection_text}\nКакого типа именения сделаем? Третьей кнопкой можно удалить ранее внесенные изменения расписания в этот день.'

    await callback.message.answer(text=txt, reply_markup=kb_c_s_type)


@router.callback_query(lambda c: c.data in ['c_s_type_0', 'c_s_type_1'])
async def put_c_s_intersection(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await callback.message.answer('Работает')

    start_date = f'{data['date']} {data['hour_start']}'
    end_date = f'{data['date']} {data['hour_end']}'

    dataBase.add_schedule_changes(start_date, end_date, '0')


@router.callback_query(F.data == 'c_s_type_2')
async def delete_c_s_intersection(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # await callback.message.answer(data['date'])
    dataBase.delete_schedule_changes(data['date'])

    txt = 'Все изменения в расписании на этот день удалены. Возвращение на панель администратора'
    await callback.message.answer(text=txt, reply_markup=kb_admin)


# @router.callback_query(F.data.startswith('c_s_type_'))
# async def put_c_s_intersection(callback: types.CallbackQuery, state: FSMContext):

