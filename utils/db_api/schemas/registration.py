from sqlalchemy import Column, BigInteger, String, sql
from utils.db_api.db_gino import TimedBaseModel


class Registration(TimedBaseModel):
    __tablename__ = 'registrations'
    user_id = Column(BigInteger, primary_key=True)  # не может повторяться в бд
    name = Column(String(200))
    username = Column(String(50))
    status = Column(String(30))
    age = Column(String(5))
    location = Column(String(20))
    affiliation = Column(String(20))

    query: sql.select
