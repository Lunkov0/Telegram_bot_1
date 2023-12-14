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
from keyboards.kAdmin import kb_admin, kb_admin_schedule
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
    builder.adjust((4))

    txt = 'Расписание на какую дату поменяем?'
    # await state.set_state(ChangeFSM.date)
    await callback.message.answer(text=txt, reply_markup=builder.as_markup())


# А теперь пляска с машиной состояний      ?????????????

# @router.callback_query(F.data.startswith('c_s_days_'))
# async def c_s_days(message: types.Message, state: FSMContext):
#     # await state.update_data(date=callback.data)
#     await state.set_state(ChangeFSM.intersection)
#     await message.answer('Отлично!!! теперь установим это говно')


@router.callback_query(F.data.startswith('c_s_days_'))
async def c_s_days(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')
    days = data[-1]
    await state.update_data(days=days)

    await callback.message.answer('Напиши, со скольки ты будешь работать в эту дату?')
    await state.set_state(ChangeFSM.intersection)
    # await ChangeFSM.intersection.set()


@router.message(ChangeFSM.intersection)
async def c_s_intersection(message: types.Message, state: FSMContext):
    # Этот кусок работает. По крайней мере, из хэндлера выше
    await message.answer('тута')
    data = await state.get_data()
    days = data.get('days')
    await message.answer(days)

    await message.answer('теперь я в нужном хэндлере')

