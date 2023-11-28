from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# btns = [
#     [
#         KeyboardButton(text='Записаться на прием'),
#         KeyboardButton(text='Мои записи'),
#     ],
# ]
#
# kb_start = ReplyKeyboardMarkup(
#     keyboard=btns,
#     resize_keyboard=True,
#     input_field_placeholder='Выберете способ подачи')  # Текст в строке ввода

# kb_start = InlineKeyboardMarkup()
# button1 = InlineKeyboardButton(text="Записаться на прием", callback_data="appointment")
# button2 = InlineKeyboardButton(text="Мои записи", callback_data="my_appointments")
# kb_start.add(button1, button2)
bt = [
    [
        InlineKeyboardButton(text="Записаться на прием", callback_data="make_an_appointment"),
        InlineKeyboardButton(text="Мои записи", callback_data="my_appointments")
    ]
]
kb_start = InlineKeyboardMarkup(
    inline_keyboard=bt,
)