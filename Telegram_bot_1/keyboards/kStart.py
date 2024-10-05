from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


bt = [
    [
        InlineKeyboardButton(text="Записаться на прием", callback_data="make_an_appointment"),
        InlineKeyboardButton(text="Мои записи", callback_data="my_appointments")
    ]
]
kb_start = InlineKeyboardMarkup(
    inline_keyboard=bt,
)