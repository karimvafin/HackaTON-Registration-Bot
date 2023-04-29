from aiogram import types

from loader import dp
from filters import IsPrivate
from keyboards.default import kb_menu
from utils.db_api import quick_commands as commands
from utils.misc import rate_limit


@rate_limit(limit=3)  # 3 секунды
@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    try:
        user = await commands.select_user(message.from_user.id)
        if user.status == 'active':
            await message.answer(f'Привет {user.first_name}\n'
                                 f'Ты уже зарегистрирован')
        elif user.status == 'banned':
            await message.answer('Ты забанен')
    except Exception:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                status='active')
        await message.answer('Ты зарегистрирован')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/ban')
async def get_ban(message: types.Message):
    await commands.update_status(message.from_user.id, 'banned')
    await message.answer('Мы тебя забанили')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/unban')
async def get_unban(message: types.Message):
    await commands.update_status(message.from_user.id, 'active')
    await message.answer('Мы тебя разбанили')


@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/profile')
async def profile(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await message.answer(f'ID: {user.user_id}\n'
                         f'First name: {user.first_name}\n'
                         f'Last name: {user.last_name}\n'
                         f'Username: {user.username}\n'
                         f'Status: {user.status}\n')
