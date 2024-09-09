from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext
import locale
from aiogram import Bot

from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import dataBase
from functions import list_to_keyboard, treatment_schedule, str_to_date, date_to_str, str_to_time, validate_phone_number
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
    await state.set_state(MakeAppointmentFSM.time)
    await callback.message.answer(text=txt, reply_markup=keyboard)


@router.callback_query(MakeAppointmentFSM.time)
async def time_make_appointment_fsm(callback: types.CallbackQuery, state: FSMContext):
    time = str_to_time(callback.data)
    await state.update_data(time=time)

    # data = await state.get_data()
    txt = f'В выбрали время: {time.time()}\nВведите номер для связи. \n\nФормат ввода: 89999999999'
    await state.set_state(MakeAppointmentFSM.phone)
    await callback.message.answer(text=txt)


@router.message(MakeAppointmentFSM.phone)
async def phone_make_appointment_fsm(message: types.Message, state: FSMContext):
    number = validate_phone_number(message.text)
    if not number:
        await state.set_state(MakeAppointmentFSM.time)
        txt = 'Не верный формат ввода номера телефона. Пожалуйста, введите еще раз.'
        await message.answer(text=txt)
    else:
        phone = message.text
        txt = f'Введен номер телефона: {phone}'
        await message.answer(text=txt)
        await state.update_data(phone=phone)
        await state.set_state(MakeAppointmentFSM.check)

@router.message(MakeAppointmentFSM.check)
async def check_make_appointment_fsm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    full_name = message.text
    appointment_time = data['time']
    contact_phone = data['phone']
    users_tg_id = message.from_user.id
    bot.send_message(user_id, 'сообщение')


''' full_name =
    appointment_time = time
    contact_phone =
    users_tg_id =
    services_id =

dataBase.add_appointment(full_name, appointment_time, contact_phone, users_tg_id, services_id)


id SERIAL PRIMARY KEY,
                full_name VARCHAR(50),
                appointment_time TIMESTAMP,
                contact_phone VARCHAR(25),
                users_tg_id VARCHAR(25),
                services_id INTEGER'''
