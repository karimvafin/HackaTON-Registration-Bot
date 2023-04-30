from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_cancel_change = ReplyKeyboardMarkup(
    keyboard=[
        # ряды кнопок
        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)
