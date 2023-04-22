from aiogram import types

from loader import dp
from filters import IsPrivate
from keyboards.default import kb_menu
from utils.misc import rate_limit


@rate_limit(limit=3)  # 3 секунды
@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    await message.answer(f'Здравствуй, {message.from_user.full_name}!', reply_markup=kb_menu)
