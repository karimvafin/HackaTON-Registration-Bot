from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import UserRegistration


@dp.message_handler(text='Мой профиль')
@dp.message_handler(commands=['profile'])
async def button_my_profile(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Ваш профиль:\n\n"
                         f"ФИО: {data.get('name')}\n"
                         f"Возраст: {data.get('age')}\n"
                         f"Город: {data.get('location')}\n"
                         f"Место работы/учебы: {data.get('affiliation')}")

