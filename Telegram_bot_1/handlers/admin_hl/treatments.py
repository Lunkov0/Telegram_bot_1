from aiogram import Router, F
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
import re

import constants
from keyboards.kAdmin import kb_admin, kb_treatments, kb_add_treatment
from database.database import dataBase
from constants import WEEKDAY
from utils.states import ChangeFSM, TreatmentFSM
from database.database import dataBase


def validate_time(time_str):
    # pattern == 0:00 - 23:59
    pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    if re.match(pattern, time_str.strip()):
        return True
    else:
        return False


def validate_integer(integer):
    # We leave only numbers and change format to the int
    res = ''.join(char for char in integer if char.isdigit())
    if res.isdigit():
        return int(res)
    else:
        return False



router = Router()


@router.callback_query(F.data == 'treatments')
async def treatments(callback: types.CallbackQuery):
    await callback.message.answer(text='Что будем делать с процедурами?', reply_markup=kb_treatments)


# Поля Процедуры для Машины состояний - name, duration, price, description
@router.callback_query(F.data == 'add_treatments')
@router.callback_query(F.data == 'change_treatment')
# @router.callback_query(F.data == 'add_treatments', F.data == 'change_treatment')
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
async def add_treatment_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    # data = await state.get_data()
    # await message.answer(text=f'name:{data['name']}, description:{data['description']}')
    await message.answer(text='Сколько по времени длится процедура? Пример формата ввода: 0:07')
    await state.set_state(TreatmentFSM.duration)


@router.message(TreatmentFSM.duration)
async def add_treatment_duration(message: types.Message, state: FSMContext):
    duration = message.text
    if validate_time(duration):
        await state.update_data(duration=message.text)
        await message.answer('Введи стоимость процедуры.')
        await state.set_state(TreatmentFSM.price)
    else:
        await message.answer('Не верный формат времени.\n введи колличество часов, двоеточие, колличество минут')
        await state.set_state(TreatmentFSM.duration)


@router.message(TreatmentFSM.price)
async def add_treatment_price(message: types.Message, state: FSMContext):
    price = message.text

    if validate_integer(price):
        await state.update_data(price=validate_integer(price))  # Каким образом лучше убрать повторение?
        await state.set_state(TreatmentFSM.final)
    else:
        await message.answer(text='Нужно ввести число в формате: 3000. Введи стоймость повторно.')
        await state.set_state(TreatmentFSM.price)

    data = await state.get_data()
    txt = (f'Отлично! Добавим процедуру со следующими параметрами?\n\n'
           f'Название процедуры: {data['name']}.\n'
           f'Описание процедуры: {data['description']}\n'
           f'Продолжительность ЧЧ:ММ: {data['duration']}.\n'
           f'Цена за процедуру: {data['price']} рублей.')
    await message.answer(text=txt, reply_markup=kb_add_treatment)


@router.message(TreatmentFSM.price)
async def add_treatment_price(callback: types.CallbackQuery, state: FSMContext):
    if callback.message.text == 'add_treatment_to_the_db':
        data = await state.get_data()
        res = [data['name'], data['duration']. data['price']. data['description']]
        dataBase.add_treatment(res)
    if callback.message.text == 'change_treatment':
        pass
