from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

import datetime

from keyboards.kAdmin import kb_admin, kb_c_s_type
from database.database import dataBase
from utils.states import ChangeFSM


router = Router()


@router.callback_query(F.data == 'change_of_schedule')
async def change_of_schedule(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    for next_day in range(30):
        # текущая день плюс число из счетчика 'next_day'
        day = datetime.date.today() + datetime.timedelta(days=next_day)
        builder.add(types.InlineKeyboardButton(text=str(day), callback_data=f'c_s_days_{str(day)}'))
    builder.adjust(3)

    all_changes = dataBase.get_all_schedule_changes()

    res = []
    for id, start_date, end_date, is_it_working_day in all_changes:
        if is_it_working_day == 0:
            type_of_day = 'выходной'
        else:
            type_of_day = 'рабочий'
        res.append(f'{str(start_date)[:-3]} до {str(end_date)[10:16]} {type_of_day} день')

    if res:
        txt = f'Текущее расписание:\n\n{'\n'.join(res)}\n\n'
    else:
        txt = ''

    txt += ('Расписание на какую дату поменяем?')
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
    await callback.message.answer(text='Напиши стартовое время для изменений',
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
    txt = f'Выбрана дата {data['date']} c {data['hour_start']} по {data['hour_end']}, какого типа именения сделаем?'

    await callback.message.answer(text=txt, reply_markup=kb_c_s_type)


@router.callback_query(lambda c: c.data in ['c_s_type_0', 'c_s_type_1'])
async def put_c_s_intersection(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    start_date = f'{data['date']} {data['hour_start']}'
    end_date = f'{data['date']} {data['hour_end']}'
    is_it_a_working_day = callback.data.split('_')[-1]

    dataBase.add_schedule_changes(start_date, end_date, is_it_a_working_day)

    if is_it_a_working_day == "0":
        txt_type_of_day = "выходной"
    else:
        txt_type_of_day = "рабочий"

    await callback.message.answer(f'В расписание записан {txt_type_of_day} день с {start_date} до {end_date}')

@router.callback_query(F.data == 'c_s_type_2')
async def delete_c_s_intersection(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    # await callback.message.answer(data['date'])
    dataBase.delete_schedule_changes(data['date'])

    txt = 'Все изменения в расписании на этот день удалены. Возвращение на панель администратора'
    await callback.message.answer(text=txt, reply_markup=kb_admin)
