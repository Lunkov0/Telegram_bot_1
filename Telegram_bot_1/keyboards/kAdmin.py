from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bt = [
    [
        InlineKeyboardButton(text="основной режим работы", callback_data="schedule"),
        InlineKeyboardButton(text="Исключения для расписания", callback_data="change_the_schedule")
    ]
]
kb_admin = InlineKeyboardMarkup(
    inline_keyboard=bt,
)

bt0 = [
    [
        # InlineKeyboardButton(text="Понедельник", callback_data="set"),
        # InlineKeyboardButton(text="Вторник", callback_data="set_schedule_1"),
        # InlineKeyboardButton(text="Среда", callback_data="set_schedule_2"),
        # InlineKeyboardButton(text="Четверг", callback_data="set_schedule_3"),
        # InlineKeyboardButton(text="Пятница", callback_data="set_schedule_4"),
        # InlineKeyboardButton(text="Суббота", callback_data="set_schedule_5"),
        # InlineKeyboardButton(text="Воскресенье", callback_data="set_schedule_6")
    ]
]
kb_admin_schedule = InlineKeyboardMarkup(
    inline_keyboard=bt0,
)
