from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

from utils.db_api.db_gino import db

# создаем бота
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

# создаем диспетчер
dp = Dispatcher(bot, storage=storage)

__all__ = ['bot', 'storage', 'dp', 'db']
