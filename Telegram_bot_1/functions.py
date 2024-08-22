import re

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram import types


def list_to_keyboard(items: list[str], columns=2) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    [
        builder.add(types.InlineKeyboardButton(
            text=item,
            callback_data=item))
        for item in items
    ]
    builder.adjust(columns)  # Кол-во столбцов

    return builder.as_markup(resize_keyboard=False)


def validate_time(time_str):
    '''pattern == 0:00 - 23:59'''
    pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    if re.match(pattern, time_str.strip()):
        return True
    else:
        return False
