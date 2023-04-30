from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery

from loader import dp
from keyboards.inline import ikb_menu
from keyboards.default import kb_cancel_change
from keyboards.default import kb_menu
from utils.db_api import registration_commands
from states import ChangeData
from utils.validate_data import check_age


@dp.message_handler(text="Изменить данные")
@dp.message_handler(Command("change_data"))
async def change_user_data(message: types.Message):
    reg = await registration_commands.select_registration_by_id(message.from_user.id)
    if reg is None:
        await message.answer(text="Вы еще не зарегистрировались\n"
                                  "Для регистрации введите /registration", reply_markup=kb_menu)
    elif reg.status == "unfinished":
        await message.answer(text="Сначала закончите регистрацию -- "
                                  "введите /registration", reply_markup=kb_menu)
    else:
        await message.answer(text="Что Вы хотите изменить?", reply_markup=ikb_menu)


@dp.message_handler(Text("Отмена"), state=[ChangeData.change_name, ChangeData.change_age,
                                           ChangeData.change_location, ChangeData.change_affiliation])
async def cancel_change_mode(message: types.Message, state: FSMContext):
    await message.answer("Изменения отменены", reply_markup=kb_menu)
    await state.finish()


@dp.callback_query_handler(text="ФИО")
async def change_name(call: CallbackQuery):
    await call.message.answer(text="Введите ФИО", reply_markup=kb_cancel_change)
    await ChangeData.change_name.set()
    # call.answer -- будет просто сообщение на экране, не в чате
    # call.message.edit_reply_markup -- для замены клавиатуры


@dp.callback_query_handler(text="Возраст")
async def change_name(call: CallbackQuery):
    await call.message.answer(text="Введите Ваш возраст", reply_markup=kb_cancel_change)
    await ChangeData.change_age.set()


@dp.callback_query_handler(text="Город")
async def change_name(call: CallbackQuery):
    await call.message.answer(text="Введите Ваш город", reply_markup=kb_cancel_change)
    await ChangeData.change_location.set()


@dp.callback_query_handler(text="Место работы")
async def change_name(call: CallbackQuery):
    await call.message.answer(text="Где Вы учитесь/работаете?", reply_markup=kb_cancel_change)
    await ChangeData.change_affiliation.set()


@dp.message_handler(state=ChangeData.change_name)
async def change_name(message: types.Message, state: FSMContext):
    answer = message.text  # ответ пользователя
    await state.update_data(change_name=answer)  # сохраняем имя пользователя
    reg = await registration_commands.select_registration_by_id(message.from_user.id)
    if reg is None:
        await message.answer(text="Вы еще не зарегистрировались\n"
                                  "Для регистрации введите /registration")
    elif reg.status == "unfinished":
        await message.answer(text="Сначала закончите регистрацию -- "
                                  "введите /registration", reply_markup=kb_menu)
    else:
        await reg.update(name=answer).apply()
        await message.answer("Данные изменены", reply_markup=kb_menu)
    await state.finish()


@dp.message_handler(state=ChangeData.change_age)
async def change_age(message: types.Message, state: FSMContext):
    answer = message.text  # ответ пользователя
    if not check_age(answer):
        await message.answer("Вы ввели некорректное число!")
        await message.answer("Введите Ваш возраст")
    else:
        await state.update_data(change_age=answer)
        reg = await registration_commands.select_registration_by_id(message.from_user.id)
        if reg is None:
            await message.answer(text="Вы еще не зарегистрировались\n"
                                      "Для регистрации введите /registration")
        elif reg.status == "unfinished":
            await message.answer(text="Сначала закончите регистрацию -- "
                                      "введите /registration", reply_markup=kb_menu)
        else:
            await reg.update(age=answer).apply()
            await message.answer("Данные изменены", reply_markup=kb_menu)
        await state.finish()


@dp.message_handler(state=ChangeData.change_location)
async def change_location(message: types.Message, state: FSMContext):
    answer = message.text  # ответ пользователя
    await state.update_data(change_location=answer)  # сохраняем имя пользователя
    reg = await registration_commands.select_registration_by_id(message.from_user.id)
    if reg is None:
        await message.answer(text="Вы еще не зарегистрировались\n"
                                  "Для регистрации введите /registration")
    elif reg.status == "unfinished":
        await message.answer(text="Сначала закончите регистрацию -- "
                                  "введите /registration", reply_markup=kb_menu)
    else:
        await reg.update(location=answer).apply()
        await message.answer("Данные изменены", reply_markup=kb_menu)
    await state.finish()


@dp.message_handler(state=ChangeData.change_affiliation)
async def change_affiliation(message: types.Message, state: FSMContext):
    answer = message.text  # ответ пользователя
    await state.update_data(change_affiliation=answer)  # сохраняем имя пользователя
    reg = await registration_commands.select_registration_by_id(message.from_user.id)
    if reg is None:
        await message.answer(text="Вы еще не зарегистрировались\n"
                                  "Для регистрации введите /registration")
    elif reg.status == "unfinished":
        await message.answer(text="Сначала закончите регистрацию -- "
                                  "введите /registration", reply_markup=kb_menu)
    else:
        await reg.update(affiliation=answer).apply()
        await message.answer("Данные изменены", reply_markup=kb_menu)
    await state.finish()
