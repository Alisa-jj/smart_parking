from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):  # регистрация
    name = State()
    surname = State()
    email = State()
    tel = State()
    password = State()


class LoginState(StatesGroup):
    email = State()
    password = State()


class AddCarState(StatesGroup):
    plate = State()
    color = State()
    model = State()