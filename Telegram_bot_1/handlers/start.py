from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.kStart import kb_start


router = Router()

@router.message(Command('start'))
async def start(message: Message):
    txt = 'Привет! Я электронный помощник, я помогу Вам с записью на прием!'
    await message.answer(txt, reply_markup=kb_start)
