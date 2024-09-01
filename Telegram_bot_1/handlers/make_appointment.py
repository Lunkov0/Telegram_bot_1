from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext
import locale

from database.database import dataBase
from functions import list_to_keyboard, treatment_schedule, str_to_date, date_to_str
from utils.states import MakeAppointmentFSM

# Установка русской локализации для модуля datetime
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)

router = Router()


@router.callback_query(F.data == 'make_an_appointment')
async def make_an_appointment(callback: types.CallbackQuery, state: FSMContext):
    treatments = dataBase.treatments_get_names()
    keyboard = list_to_keyboard([val[1] for val in treatments])
    await state.set_state(MakeAppointmentFSM.treatment)

    await callback.message.answer(text='Выберите процедуру', reply_markup=keyboard)


@router.callback_query(MakeAppointmentFSM.treatment)
async def m_a_treatment(callback: types.CallbackQuery, state: FSMContext):
    treatment = callback.data
    await state.update_data(treatment=treatment)

    schedule = treatment_schedule(treatment)
    await state.update_data(schedule=schedule)

    keyboard = list_to_keyboard([str(day) for day in schedule if schedule[day]], 3)

    txt = 'Вы выбрали процедуру: ' + treatment + ('.\nНиже показаны даты где есть свободное время.'
                                                  ' Нажмите, чтобы увидеть сободные часы для записи.')

    await state.set_state(MakeAppointmentFSM.schedule)
    await callback.message.answer(text=txt, reply_markup=keyboard)


@router.callback_query(MakeAppointmentFSM.schedule)
async def schedule_make_appointment_fsm(callback: types.CallbackQuery, state: FSMContext):
    day = callback.data
    schedule = await state.get_data()
    schedule = schedule.get('schedule')

    txt = f'Вы выбрали дату: {day}, ниже показано свободное для записи время на этот день.'

    day = str_to_date(day)
    await state.update_data(day=day)

    keyboard = list_to_keyboard(schedule[day])

    await callback.message.answer(text=txt, reply_markup=keyboard)


@router.message(F.text == '333')
@router.callback_query(F.data.startswith('make_an_appointment_'))
async def some(message: types.Message):
    keyboard = list_to_keyboard(['1', '2', '3', '4', '5', '6', '3', '3', '41', '2', '5'], 3)
    await message.answer(text='Some активирован!!!', reply_markup=keyboard)
