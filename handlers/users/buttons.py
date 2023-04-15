from aiogram import types

from loader import dp


@dp.message_handler(text='Мой профиль')
async def button_my_profile(message: types.Message):
    await message.answer(f"Ваш профиль:\n"
                         f" ID: {message.from_user.id}\n"
                         f" ФИО: {message.from_user.full_name}\n"
                         f" Возраст: 100\n"
                         f" Город: Долгопрудный\n"
                         f" Место работы: mmcp")

