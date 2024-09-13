from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext
import locale
from aiogram import Bot

from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import dataBase
from functions import list_to_keyboard, treatment_schedule, str_to_date, date_to_str, str_to_time, validate_phone_number
from keyboards.kStart import kb_start
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
        txt = f'Введен номер телефона: {phone}\n\nВведите ФИО'
        await message.answer(text=txt)
        await state.update_data(phone=phone)
        await state.set_state(MakeAppointmentFSM.name)


@router.message(MakeAppointmentFSM.name)
async def name_make_appointment_fsm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    full_name = message.text
    user_id = message.from_user.id
    await state.update_data(name=full_name)
    await state.update_data(user_id=user_id)
    time = data['time']
    phone = data['phone']
    treatment = data['treatment']

    txt = (f'Вы ввели данные:\n\nФИО: {full_name}\nТелефон: {phone}\nПроцедура: {treatment}\n'
           f'Время записи: {time.time()}\n\nДля потверждения данных нажмите Записаться')

    keyboard = list_to_keyboard(['Записаться', 'Отмена'])
    await message.answer(text=txt, reply_markup=keyboard)
    await state.set_state(MakeAppointmentFSM.check)


@router.callback_query(MakeAppointmentFSM.check)
async def check_make_appointment_fsm(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'Отмена':
        txt = 'Запись на процедуру отменена. Для продолжения, выберете команду /start в Меню бота'
        await callback.message.answer(text=txt)
    if callback.data == 'Записаться':
        data = await state.get_data()
        name = data['name']
        user_id = data['user_id']
        time = data['time']
        phone = data['phone']
        treatment = data['treatment']
        treatment_id = dataBase.get_treatment_id(treatment)[0]
        dataBase.add_appointment(name, time, phone, user_id, treatment_id)
        txt = 'Вы успешно записались на прием! Данные о своей записи вы можете посмотреть в разделе "Мои записи.'
        await callback.message.answer(text=txt, reply_markup=kb_start)


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
