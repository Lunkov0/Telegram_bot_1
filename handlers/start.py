from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.kStart import kb_start


router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        'Привет! Я электронный помощник, я помогу Вам с записью на прием!',
        reply_markup=kb_start
    )
