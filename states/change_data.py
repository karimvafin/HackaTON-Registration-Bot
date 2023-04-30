from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeData(StatesGroup):
    change_name = State()
    change_age = State()
    change_location = State()
    change_affiliation = State()
