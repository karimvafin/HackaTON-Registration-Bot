from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegistration(StatesGroup):
    name = State()
    age = State()
    location = State()
    affiliation = State()


class Accept(StatesGroup):
    user_id = State()
