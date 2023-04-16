from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from loader import dp
from keyboards.default import kb_menu
from keyboards.default import kb_end_registration
from states import UserRegistration


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
    await state.update_data(name=answer) # сохраняем имя пользователя
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
    await message.answer(f"Ваш профиль:\n"
                         f"\n"
                         f"ФИО: {data.get('name')}\n"
                         f"Возраст: {data.get('age')}\n"
                         f"Город: {data.get('location')}\n"
                         f"Место работы/учебы: {data.get('affiliation')}")
