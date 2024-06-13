from pydoc import html

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm import state

import datetime

import constants
from database.database import dataBase
from keyboards.kAdmin import kb_admin, kb_admin_schedule, kb_c_s_type
from database.database import dataBase
from constants import WEEKDAY
from utils.states import ChangeFSM

router = Router()


@router.message(F.text == '123')
async def admin_p(message: Message):
    await message.answer(
        'Это админ панель.\n\nЗдесь ты можешь настроить стандартное расписание (для каждого дня недели'
        ' выставляется график работы)\n\nИсключения для рассписания (на конкретную дату добавляется'
        ' дополнительное рабочее время или наоборот убирается)',
        reply_markup=kb_admin,
    )


# Как убрать повторение?
@router.callback_query(F.data == 'back_to_admin')
async def admin_p2(callback: CallbackQuery):
    await callback.message.answer(
        'Это админ панель.\n\nЗдесь ты можешь настроить стандартное расписание (для каждого дня недели'
        ' выставляется график работы)\n\nИсключения для рассписания (на конкретную дату добавляется'
        ' дополнительное рабочее время или наоборот убирается)',
        reply_markup=kb_admin,
    )
