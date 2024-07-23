from aiogram import Router, F
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

import constants
from keyboards.kAdmin import kb_admin, kb_type_of_schedule
from database.database import dataBase
from constants import WEEKDAY
from utils.states import ConstantBreaksFSM
from handlers.admin_hl.treatments import validate_time


router = Router()


@router.message(ConstantBreaksFSM.start_time)
async def start_time_constant_breaks(message: types.Message, state: FSMContext):
    start_time = message.text
    if validate_time(start_time):
        await state.update_data(start_time=start_time)
        await message.answer('Теперь введи время, когда перерыв будет заканчиваться')
        await state.set_state(ConstantBreaksFSM.end_time)
    else:
        await message.answer('Неверный формат времени. Введи еще раз.')
        await state.set_state(ConstantBreaksFSM.start_time)


@router.message(ConstantBreaksFSM.end_time)
async def end_time_constant_breaks(message: types.Message, state: FSMContext):
    end_time = message.text
    if validate_time(end_time):
        await state.update_data(end_time=end_time)
        dataBase.delete_table_constant_breaks()

        data = await state.get_data()

        start_time = data['start_time'] + ':00'
        end_time = data['end_time'] + ':00'

        dataBase.add_constant_breaks(start_time, end_time)
        txt = f'Постоянный перерыв успешно добавлен!\n\nПерерыв с {data['start_time']} до {data['end_time']}'
        await message.answer(text=txt)
    else:
        await message.answer('Неверный формат времени. Введи еще раз.')
        await state.set_state(ConstantBreaksFSM.end_time)