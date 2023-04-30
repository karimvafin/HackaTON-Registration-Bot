from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins
from filters import IsPrivate
from loader import dp
from keyboards.default import kb_menu
from keyboards.default import kb_end_registration
from states import UserRegistration
from states.user_registration import Accept
from utils.db_api import registration_commands
from utils.misc import rate_limit
from utils.validate_data import check_age


async def continue_registration(reg):
    if reg.name == 'None':
        await UserRegistration.name.set()
        return "Введите Ваше ФИО"
    elif reg.age == 'None':
        await UserRegistration.age.set()
        return "Сколько Вам лет?"
    elif reg.location == 'None':
        await UserRegistration.location.set()
        return "Из какого Вы города?"
    elif reg.name == 'None':
        await UserRegistration.affiliation.set()
        return "Где Вы работаете/учитесь?"


@rate_limit(limit=3)
@dp.message_handler(Text('Регистрация'))
@dp.message_handler(Command('registration'))
async def button_registration(message: types.Message):
    reg = await registration_commands.select_registration_by_id(message.from_user.id)
    if reg is None:
        await message.answer(f'Начало регистрации\nВведите Ваше ФИО', reply_markup=kb_end_registration)
        await UserRegistration.name.set()
    else:
        if reg.status == "created":
            await message.answer("Вы уже зарегистрированы!\n"
                                 "Для просмотра профиля, введите /profile\n"
                                 "Чтобы изменить свои данные, введите /change_data")
        elif reg.status == "unfinished":
            await message.answer("Продолжение регистрации\n")
            await message.answer(await continue_registration(reg), reply_markup=kb_end_registration)


@dp.message_handler(Text("Приостановить регистрацию"), state=[UserRegistration.name, UserRegistration.age,
                                                              UserRegistration.location, UserRegistration.affiliation])
async def stop_registration(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    age = data.get('age')
    location = data.get('location')
    affiliation = data.get('affiliation')
    if name is None:
        name = "None"
    if age is None:
        age = "None"
    if location is None:
        location = "None"
    if affiliation is None:
        affiliation = "None"
    reg = await registration_commands.select_registration_by_id(message.from_user.id)
    if reg is None:
        await registration_commands.register_user(user_id=message.from_user.id,
                                                  name=name,
                                                  username=message.from_user.username,
                                                  status='unfinished',
                                                  age=age,
                                                  location=location,
                                                  affiliation=affiliation)
    else:
        if reg.name == "None":
            await reg.update(name=name).apply()
        if reg.age == "None":
            await reg.update(age=age).apply()
        if reg.location == "None":
            await reg.update(location=location).apply()
        if reg.affiliation == "None":
            await reg.update(affiliation=affiliation).apply()

    await state.finish()
    await message.answer(text="Регистрация приостановлена.\n"
                              "Чтобы продолжить регистрацию, введите команду /registration.", reply_markup=kb_menu)


@dp.message_handler(state=UserRegistration.name)
async def get_name(message: types.Message, state: FSMContext):
    answer = message.text  # ответ пользователя
    await state.update_data(name=answer)  # сохраняем имя пользователя
    await message.answer("Cколько Вам лет?")
    await UserRegistration.age.set()


@dp.message_handler(state=UserRegistration.age)
async def get_age(message: types.Message, state: FSMContext):
    answer = message.text  # ответ пользователя
    if not check_age(answer):
        await message.answer("Вы ввели некорректное число!")
        await message.answer("Сколько Вам лет?")
    else:
        await state.update_data(age=answer)  # сохраняем имя пользователя
        await message.answer("Из какого Вы города?")
        await UserRegistration.location.set()


@dp.message_handler(state=UserRegistration.location)
async def get_location(message: types.Message, state: FSMContext):
    answer = message.text  # ответ пользователя
    await state.update_data(location=answer)  # сохраняем имя пользователя
    await message.answer("Где Вы работаете/учитесь?")
    await UserRegistration.affiliation.set()


@dp.message_handler(state=UserRegistration.affiliation)
async def get_affiliation(message: types.Message, state: FSMContext):
    answer = message.text  # ответ пользователя
    await state.update_data(affiliation=answer)  # сохраняем имя пользователя
    data = await state.get_data()
    await state.finish()
    await message.answer(f"Регистрация успешно завершена!", reply_markup=kb_menu)
    name = data.get('name')
    age = data.get('age')
    location = data.get('location')
    affiliation = data.get('affiliation')
    reg = await registration_commands.select_registration_by_id(message.from_user.id)
    if reg is None:
        await registration_commands.register_user(user_id=message.from_user.id,
                                                  name=name,
                                                  username=message.from_user.username,
                                                  status='created',
                                                  age=age,
                                                  location=location,
                                                  affiliation=affiliation)
    else:
        if reg.name == "None":
            await reg.update(name=name).apply()
        if reg.age == "None":
            await reg.update(age=age).apply()
        if reg.location == "None":
            await reg.update(location=location).apply()
        if reg.affiliation == "None":
            await reg.update(affiliation=affiliation).apply()
        await reg.update(status='created').apply()

    reg = await registration_commands.select_registration_by_id(message.from_user.id)
    await message.answer(f"Ваш профиль:\n"
                         f"\n"
                         f"ФИО: {reg.name}\n"
                         f"Возраст: {reg.age}\n"
                         f"Город: {reg.location}\n"
                         f"Место работы/учебы: {reg.affiliation}")


@dp.message_handler(IsPrivate(), text='/registrations', user_id=admins)
async def get_reg(message: types.Message):
    try:
        reg = await registration_commands.select_registration()
        ikb = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text='Accept',
                                                                callback_data='Accept')
                                       ]
                                   ])
        await message.answer(f'Дата создания: {reg.created_at}\n'
                             f'id: {reg.user_id}\n'
                             f'name: {reg.name}\n'
                             f'username: {reg.username}\n'
                             f'age: {reg.age}\n'
                             f'location: {reg.location}\n'
                             f'affiliation: {reg.affiliation}\n',
                             reply_markup=ikb)
    except Exception:
        await message.answer('Нет новых регистраций')


@dp.callback_query_handler(text='Accept')
async def accept_reg(call: types.CallbackQuery):
    await call.message.answer(f'Введите id для подтверждения')
    await Accept.user_id.set()


@dp.message_handler(state=Accept.user_id)
async def accept_reg(message: types.Message, state: FSMContext):
    # TODO cast сообщения к int
    await registration_commands.accept_registration(int(message.text))
    await message.answer(f'Подтвержден: {message.text}')
    await state.finish()
