from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.kStart import kb_start, kb_step


router = Router()

@router.message(F.text.lower() == 'Записаться на прием')
async def button1(message: Message):
    await message.answer(
        'Ты нажал первую кнопку',
        reply_markup=kb_step)