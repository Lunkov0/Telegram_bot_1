from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

# from keyboards.kStart import
from database.database import dataBase


router = Router()


@router.callback_query(F.data == 'make_an_appointment')
async def make_an_appointment(callback: types.CallbackQuery):
    treatments = dataBase.treatments_get_names()

    builder = InlineKeyboardBuilder()
    for service_id, service in treatments:
        builder.add(types.InlineKeyboardButton(text=service, callback_data=f'make_an_appointment_{service_id}'))
    builder.adjust(2)  # Кол-во столбцов

    await callback.message.answer(text='Выберете процедуру', reply_markup=builder.as_markup(resize_keyboard=False))


@router.callback_query(F.data == 'make_an_appointment')
async def m_a_treatment(callback: types.CallbackQuery):
    txt = 'Вы выбрали процедуру'
