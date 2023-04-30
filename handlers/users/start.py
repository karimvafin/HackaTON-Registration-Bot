from aiogram import types

from loader import dp
from filters import IsPrivate
from keyboards.default import kb_menu
from utils.misc import rate_limit
from utils.db_api import quick_commands as commands


@rate_limit(limit=3)  # 3 секунды
@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    if user is None:
        await commands.add_user(user_id=message.from_user.id,
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                status='active')
    await message.answer(text=f"Привет, {message.from_user.first_name} {message.from_user.last_name}!\n\n"
                              f"Это бот Souldev Hacks для сопровождения участников хакатона\n\n"
                              f"Нажми /menu, чтобы открыть меню")
