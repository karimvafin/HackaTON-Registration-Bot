from aiogram import types

from loader import dp
from keyboards.default import kb_menu
from keyboards.default import kb_end_registration


@dp.message_handler(text='Регистрация')
async def button_registration(message: types.Message):
    await message.answer(f'Начало регистрации', reply_markup=kb_end_registration)


@dp.message_handler(text="Приостановить регистрацию")
async def stop_registration(message: types.Message):
    await message.answer(text="Регистрация приостановлена. \n "
                              "Чтобы продолжить регистрацию, напишите Регистрация.", reply_markup=kb_menu)
