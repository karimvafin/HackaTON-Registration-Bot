from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemas.registration import Registration


async def register_user(user_id: int, name: str, username: str, status: str, age: str,
                        location: str, affiliation: str):
    try:
        registration = Registration(user_id=user_id, name=name, username=username,
                                    status=status, age=age, location=location, affiliation=affiliation)
        await registration.create()
    except UniqueViolationError:
        print('Регистрация не удалась')





async def select_registration():
    registration = await Registration.query.where(Registration.status == 'created').gino.first()
    return registration


async def select_registration_by_id(user_id: int):
    registration = await Registration.query.where(Registration.user_id == user_id).gino.first()
    return registration


async def accept_registration(user_id: int):
    registration = await select_registration_by_id(user_id)
    await registration.update(status='accepted').apply()


async def update_registration(reg, new_name: str, new_age: str, new_location: str, new_affiliation: str):
    await reg.update(name=new_name).apply()
    await reg.update(age=new_age).apply()
    await reg.update(location=new_location).apply()
    await reg.update(affiliation=new_affiliation).apply()
