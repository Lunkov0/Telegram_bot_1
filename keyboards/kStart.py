from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


btns = [
    [
        KeyboardButton(text='Записаться на прием'),
        KeyboardButton(text='Мои записи'),
    ],
]

kb_start = ReplyKeyboardMarkup(
    keyboard=btns,
    resize_keyboard=True,
    input_field_placeholder='Выберете способ подачи')  # Текст в строке ввода

btns2 = [
    [KeyboardButton(text='Step1'),
     KeyboardButton(text='Step2')]
]

kb_step = ReplyKeyboardMarkup(
    keyboard=btns2,
    resize_keyboard=True,
    input_field_placeholder='Второй шаг',
)
