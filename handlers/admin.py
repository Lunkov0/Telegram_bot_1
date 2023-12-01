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

# Пишет текущее расписание. Выдает дни недели для смены расписания.
@router.callback_query(F.data == 'schedule')
async def schedule(callback: types.CallbackQuery):
    s = dataBase.schedule_get()
    weekday = [i for i in range(7)]
    for i, num, start, stop in s:
        weekday[int(num)] = f'{constants.WEEKDAY[int(num)]}: с {str(start)[:5]} до {str(stop)[:5]}'

    builder = InlineKeyboardBuilder()
    for num, day in constants.WEEKDAY.items():
        builder.add(types.InlineKeyboardButton(text=day, callback_data=f'schedule_set_{num}'))
    builder.adjust(2)  # Кол-во столбцов)

    txt = 'Твоё текущее расписание:\n\n' + '\n'.join(weekday) + '\n\n Кнопками ниже можно изменить часы работы'
    await callback.message.answer(text=txt, reply_markup=builder.as_markup(resize_keyboard=False))


@router.callback_query(F.data[:13].as_('set_schedule_'))
async def schedule_set(callback: types.CallbackQuery):
    await callback.message.answer(text=f'Hallo {callback.data}')
