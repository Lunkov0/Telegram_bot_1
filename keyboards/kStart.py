from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb_start = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Записаться на прием',
            callback_data='make_an_appointment'
        )

    ],
    [
        InlineKeyboardButton(
            text='Просмотреть мои записи',
            callback_data='my_appointments'
        )
    ]
])
