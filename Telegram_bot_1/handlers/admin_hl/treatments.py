from aiogram import Router, F
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

import constants
from keyboards.kAdmin import kb_admin, kb_treatments
from database.database import dataBase
from constants import WEEKDAY
from utils.states import ChangeFSM, TreatmentFSM
from database.database import dataBase

router = Router()


@router.callback_query(F.data == 'treatments')
async def treatments(callback: types.CallbackQuery):
    await callback.message.answer(text='Что будем делать с процедурами?', reply_markup=kb_treatments)



# Поля Процедуры для Машины состояний - name, duration, price, description
@router.callback_query(F.data == 'add_treatments')
async def add_treatments(callback: types.CallbackQuery, state: FSMContext):
    txt = dataBase.treatments_get_names()
    await callback.message.answer(text=f'Введи краткое название добавляемой процедуры\n{txt}')
    await state.set_state(TreatmentFSM.name)


@router.message(TreatmentFSM.name)
async def add_treatment_name(message: types.Message, state: FSMContext):
    await message.answer(text='Добавь описание к процедуре')
    await state.update_data(name=message.text)
    await state.set_state(TreatmentFSM.description)


@router.message(TreatmentFSM.description)
async def add_treatment_price(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await message.answer(text=f'name:{data['name']}, description:{data['description']}')
    # await message.answer(text='Работает')
