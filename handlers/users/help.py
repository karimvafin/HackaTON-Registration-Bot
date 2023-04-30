from aiogram import types
from loader import dp


@dp.message_handler(text='/help')
async def command_help(message: types.Message):
    await message.answer(f'Вот список команд, которые ты можешь отправить боту:\n\n'
                         f'/menu -- открыть меню\n'
                         f'/registration -- начать или продолжить регистрацию\n'
                         f'/profile -- посмотреть свой профиль\n'
                         f'/change_data -- изменить данные')
