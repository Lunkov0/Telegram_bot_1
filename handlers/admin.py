from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import dataBase
from keyboards.kAdmin import kb_admin

router = Router()


@router.message(F.text.lower() == '123')
async def admin_p(message: Message):
    await message.answer(
        'Ты нажал вторую кнопку',
        reply_markup=kb_admin,
    )