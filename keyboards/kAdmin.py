from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


bt = [
    [
        InlineKeyboardButton(text="основной режим работы", callback_data="make_an_appointment"),
        InlineKeyboardButton(text="Исключения для расписания", callback_data="my_appointments")
    ]
]
kb_admin = InlineKeyboardMarkup(
    inline_keyboard=bt,
)