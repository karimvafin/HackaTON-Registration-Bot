from aiogram import types

from loader import dp
from utils.db_api import registration_commands


@dp.message_handler(text='Мой профиль')
@dp.message_handler(commands=['profile'])
async def button_my_profile(message: types.Message):
    try:
        reg = await registration_commands.select_registration_by_id(message.from_user.id)
        await message.answer(f"Ваш профиль:\n\n"
                             f"ФИО: {reg.name}\n"
                             f"Возраст: {reg.age}\n"
                             f"Город: {reg.location}\n"
                             f"Место работы/учебы: {reg.affiliation}")
    except Exception:
        await message.answer("Вы еще не зарегистрировались.\n"
                             "Для регистрации отправьте команду /registration")
