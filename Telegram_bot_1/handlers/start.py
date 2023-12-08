from aiogram import Router, F
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

@router.message(F.text.lower() == 'button2')
async def button2(message: Message):
    await message.reply('Ты нажал вторую кнопку')

@router.message(F.text.lower() == 'step1')
async def step1(message: Message):
    await message.reply('Ты нажал кнопку step1')


@router.message(F.text.lower() == 'step2')
async def step2(message: Message):
    await message.reply('Ты нажал кнопку Step2')
