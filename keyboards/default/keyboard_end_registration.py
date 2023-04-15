from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_end_registration = ReplyKeyboardMarkup(
    keyboard=[
        # ряды кнопок
        [
            KeyboardButton(text='Приостановить регистрацию')
        ]
    ],
    resize_keyboard=True
)
