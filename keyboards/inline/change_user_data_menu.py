from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_menu = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="ФИО", callback_data="ФИО"),
        InlineKeyboardButton(text="Возраст", callback_data="Возраст")
    ],
    [
        InlineKeyboardButton(text="Город", callback_data="Город"),
        InlineKeyboardButton(text="Место учебы/работы", callback_data="Место работы")
    ]
])
