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


@rate_limit(limit=3)
@dp.message_handler(Text('Регистрация'))
@dp.message_handler(Command('registration'))
async def button_registration(message: types.Message):
    await message.answer(f'Начало регистрации\nВведите Ваше ФИО', reply_markup=kb_end_registration)
    await UserRegistration.name.set()


@dp.message_handler(Text("Приостановить регистрацию"), state=[UserRegistration.name, UserRegistration.age,
                                                              UserRegistration.location, UserRegistration.affiliation])
async def stop_registration(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Регистрация приостановлена. \n "
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
    if not answer.isdigit() or answer[0] == '0' or int(answer) < 1:
        await message.answer("Вы ввели некорректное число!")
        await message.answer("Сколько Вам лет?")
    else:
        await state.update_data(age=answer)  # сохраняем имя пользователя
        await message.answer("Из каково Вы города?")
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
    await registration_commands.register_user(user_id=message.from_user.id,
                                              name=name,
                                              username=message.from_user.username,
                                              status='created',
                                              age=age,
                                              location=location,
                                              affiliation=affiliation)
    await message.answer(f"Ваш профиль:\n"
                         f"\n"
                         f"ФИО: {data.get('name')}\n"
                         f"Возраст: {data.get('age')}\n"
                         f"Город: {data.get('location')}\n"
                         f"Место работы/учебы: {data.get('affiliation')}")


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
