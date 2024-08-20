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
