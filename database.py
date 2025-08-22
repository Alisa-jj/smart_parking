from sqlalchemy import create_engine, Table, Column, Integer, BigInteger, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

Base = declarative_base()

user_car = Table(
    'users_cars',
    Base.metadata,
Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('car_id', Integer, ForeignKey('cars.id', ondelete='CASCADE'), primary_key=True)
)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    sername = Column(String(32), nullable=False)
    password = Column(String(512), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    tel = Column(String(16), nullable=True, unique=True)

cars = relationship('Cars', secondary='user.car', back_populates='users')

def __repr__(self):
    return f"<{self.name}, {self.sername}>"


class Cars(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    plate = Column(String(16), nullable=False, unique=True)
    color = Column(String(16), nullable=False)
    model = Column(String(32), nullable=False)
    status = Column(Boolean, nullable=False)

users = relationship('Users', secondary='users.car', back_populates='cars')

def __repr__(self):
    return f"<{self.model}, {self.color}, {self.plate}>"


class Parking(Base):
    __tablename__ = 'parking'

    car_id = Column(Integer, ForeignKey('cars.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    entertime = Column(DateTime)
    exittime = Column(DateTime)
