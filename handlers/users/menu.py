from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from keyboards.default import kb_menu


@dp.message_handler(Command("menu"))
async def menu(message: types.Message):
    await message.answer("Выберите опцию", reply_markup=kb_menu)
