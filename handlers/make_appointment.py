from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types

# from keyboards.kStart import


router = Router()


@router.callback_query(F.data == 'make_an_appointment')
async def make_an_appointment(callback: types.CallbackQuery):
    # await callback.message.answer
    await callback.message.answer(text='Some')
