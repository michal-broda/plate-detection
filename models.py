from sqlalchemy import Column, MetaData, Date, String, Integer, Boolean
from sqlalchemy.orm import declarative_base

_metadata = MetaData()
Base = declarative_base(metadata=_metadata)


# alembic revision --autogenerate -m "Intial tables"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False )
    email = Column(String(100), nullable=False)
    admin = Column(Boolean, default=True)


class Plate(Base):
    __tablename__ = "plates"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    hour = Column(String(10), nullable=False )
    plate = Column(String(10), nullable=False)
    image = Column(String(100))


# Podziel users i plate na dwie tabele

