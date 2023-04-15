from aiogram import types
from loader import dp


@dp.message_handler(text='/hello')
async def command_hello(message: types.Message):
    await message.answer(f'Здравствуй, {message.from_user.full_name}!')
