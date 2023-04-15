from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        # ряды кнопок
        [
            KeyboardButton(text='Регистрация')
        ],
        [
            KeyboardButton(text='Мой профиль')
        ],
        [
            KeyboardButton(text='Изменить данные')
        ]
    ],
    resize_keyboard=True
)
