from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import datetime

# from keyboards.kStart import
from database.database import dataBase


router = Router()


def appointment_time():
    weekday = datetime.date.today().weekday()



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
    t = datetime.date.today().weekday()
    await message.answer(text=str(t))
    txt = str(dataBase.get_weekday_schedule(t))
    await message.answer(text=txt)
