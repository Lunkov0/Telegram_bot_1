from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bt = [
    [
        InlineKeyboardButton(text='Основной режим работы', callback_data='schedule_type')
    ],
    [
        InlineKeyboardButton(text='Исключения для расписания', callback_data='change_of_schedule'),
    ],
    [
        InlineKeyboardButton(text='Управление процедурами', callback_data='treatments'),
    ],
]
kb_admin = InlineKeyboardMarkup(
    inline_keyboard=bt,
)

bt4 = [
    [
        InlineKeyboardButton(text='Основное рабочее время', callback_data='schedule')
    ],
    [
        InlineKeyboardButton(text='Постоянные перерывы', callback_data='constant_breaks'),
    ],
]
kb_type_of_schedule = InlineKeyboardMarkup(
    inline_keyboard=bt4,
)

bt0 = [
    [
        # InlineKeyboardButton(text='Понедельник', callback_data='set'),
        # InlineKeyboardButton(text='Вторник', callback_data='set_schedule_1'),
        # InlineKeyboardButton(text='Среда', callback_data='set_schedule_2'),
        # InlineKeyboardButton(text='Четверг', callback_data='set_schedule_3'),
        # InlineKeyboardButton(text='Пятница', callback_data='set_schedule_4'),
        # InlineKeyboardButton(text='Суббота', callback_data='set_schedule_5'),
        # InlineKeyboardButton(text='Воскресенье', callback_data='set_schedule_6')
    ]
]
kb_admin_schedule = InlineKeyboardMarkup(
    inline_keyboard=bt0,
)

bt1 = [
    [
        InlineKeyboardButton(text='Выходной!', callback_data='c_s_type_0'),
        InlineKeyboardButton(text='Рабочий', callback_data='c_s_type_1'),
        InlineKeyboardButton(text='Удалить', callback_data='c_s_type_2'),
    ]
]

kb_c_s_type = InlineKeyboardMarkup(
    inline_keyboard=bt1,
)


bt2 = [
    [
        InlineKeyboardButton(text='Добавить', callback_data='add_treatments'),
        InlineKeyboardButton(text='Удалить', callback_data='delete_treatments'),
    ],
]

kb_treatments = InlineKeyboardMarkup(
    inline_keyboard=bt2,
)


bt3 = [
    [
        InlineKeyboardButton(text='Добавляем!', callback_data='add_treatment_to_the_db'),
    ],
    [
        InlineKeyboardButton(text='Ввести заново', callback_data='change_treatment'),
    ],
    [
        InlineKeyboardButton(text='Отменить', callback_data='back_to_admin'),
    ]
]

kb_add_treatment = InlineKeyboardMarkup(
    inline_keyboard=bt3,
)
