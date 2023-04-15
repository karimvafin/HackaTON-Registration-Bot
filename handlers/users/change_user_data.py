from aiogram import types
from aiogram.types import CallbackQuery

from loader import dp
from keyboards.inline import ikb_menu


@dp.message_handler(text="Изменить данные")
async def change_user_data(message: types.Message):
    await message.answer(text="Что Вы хотите изменить?", reply_markup=ikb_menu)


@dp.callback_query_handler(text="ФИО")
async def change_name(call: CallbackQuery):
    await call.message.answer(text="Введите ФИО")
    # call.answer -- будет просто сообщение на экране, не в чате
    # call.message.edit_reply_markup -- для замены клавиатуры
