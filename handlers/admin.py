from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

import constants
from database.database import dataBase
from keyboards.kAdmin import kb_admin, kb_admin_schedule
from database.database import dataBase

router = Router()


@router.message(F.text.lower() == '123')
async def admin_p(message: Message):
    await message.answer(
        'Это админ панель.\n\nЗдесь ты можешь настроить стандартное расписание (для каждого дня недели выставляется график работы)\n\nИсключения для рассписания (на конкретную дату добавляется дополнительное рабочее время или наоборот убирается)',
        reply_markup=kb_admin,
    )

@router.callback_query(F.data == 'schedule')
async def schedule(callback: types.CallbackQuery):
    s = dataBase.schedule_get()

    builder = InlineKeyboardBuilder()
    for num, day in constants.WEEKDAY.items():
        builder.add(types.InlineKeyboardButton(text=day, callback_data=f'schedule_set_{num}'))
    builder.adjust(2)  # Кол-во столбцов)

    await callback.message.answer(text='Тут надо распарсить "s"', reply_markup=builder.as_markup(resize_keyboard=False))
