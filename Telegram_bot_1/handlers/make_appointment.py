from datetime import datetime, date, timedelta

from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext
import locale

from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.database import dataBase
from functions import list_to_keyboard, treatment_schedule, str_to_date, date_to_str, str_to_time, validate_phone_number
from keyboards.kStart import kb_start
from utils.states import MakeAppointmentFSM

# Установка русской локализации для модуля datetime
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)

router = Router()


@router.callback_query(F.data == 'my_appointments')
async def make_an_appointments(callback: types.CallbackQuery, state: FSMContext):
    try:
        appointments = dataBase.get_my_appointments(callback.from_user.id)[0]
        treatment = dataBase.get_treatment_name(appointments[5])
        txt = f'{appointments[1]}, Вы записаны на процедуру"{treatment[0]}". Дата приёма: {appointments[2]}'
    except IndexError:
        txt = 'Сейчас у Вас нет записей. Можете записаться с помощью этого бота!'

    await callback.message.answer(text=txt, reply_markup=kb_start)


@router.callback_query(F.data == 'make_an_appointment')
async def make_an_appointment(callback: types.CallbackQuery, state: FSMContext):
    appointment = dataBase.get_my_appointments(callback.from_user.id)
    if appointment:
        appointment = appointment[0]
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text='Удалить', callback_data='delete_my_appointment'))
        keyboard = builder.as_markup(resize_keyboard=False)

        appointment_name = dataBase.get_treatment_name(appointment[5])[0]
        date = appointment[2]
        txt = (f'В данный момент можно записаться только на одну процедуру.\n\n'
               f'Вы записаны на процедуру "{appointment_name}" Дата: {date_to_str(date)}.'
               f'Вы можете изменить данные по вашей записи не позднее чем два дня до приема,'
               f' для этого удалите предыдущую запись.')
        await state.set_state(MakeAppointmentFSM.delete)
    else:
        treatments = dataBase.treatments_get_names()
        keyboard = list_to_keyboard([val[1] for val in treatments])
        await state.set_state(MakeAppointmentFSM.treatment)
        txt = 'Выберите процедуру.'

    await callback.message.answer(text=txt, reply_markup=keyboard)


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
        txt = 'Не верный формат ввода номера телефона. Пожалуйста, введите еще раз.'
        await message.answer(text=txt)
        await state.set_state(MakeAppointmentFSM.phone)
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
        day = data['day']
        time = datetime.combine(day, time.time())
        phone = data['phone']
        treatment = data['treatment']
        treatment_id = dataBase.get_treatment_id(treatment)[0]
        dataBase.add_appointment((name, time, phone, user_id, treatment_id))
        txt = 'Вы успешно записались на прием! Данные о своей записи вы можете посмотреть в разделе "Мои записи.'
        await callback.message.answer(text=txt, reply_markup=kb_start)


@router.callback_query(MakeAppointmentFSM.delete)
async def delete_appointment_fsm(callback: types.CallbackQuery, state: FSMContext):
    keyboard = list_to_keyboard(['Подтвердить', 'Отмена'])
    txt = 'Вы уверены что хотите удалить текущую запись?'
    await state.set_state(MakeAppointmentFSM.confirm)
    await callback.message.answer(text=txt, reply_markup=keyboard)


@router.callback_query(MakeAppointmentFSM.confirm)
async def confirm_appointment_fsm(callback: types.CallbackQuery):
    if callback.data == 'Отмена':
        await callback.message.answer(text='Отмена. Возвращение на стартовое диалоговое окно.', reply_markup=kb_start)
    if callback.data == 'Подтвердить':
        user_id = callback.from_user.id

        my_appointment = dataBase.get_my_appointments(callback.from_user.id)
        if my_appointment:
            my_appointment = my_appointment[0]
            appointment_time = my_appointment[2].date()
            now = date.today()
            delt = timedelta(days=2)
            min_date_for_canceling = now + delt
            if appointment_time > min_date_for_canceling:
                dataBase.del_appointment(user_id)
                await callback.message.answer(text='Запись удалена. Возвращение на стартовое диалоговое окно.',
                                              reply_markup=kb_start)
            else:
                txt = 'Запись на прием можно отменить за два и более дня. Для отмены. обратитесь к администратору'
                await callback.message.answer(text=txt, reply_markup=kb_start)


