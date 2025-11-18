import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from db import SessionLocal, init_db, Users, Cars
from werkzeug.security import generate_password_hash, check_password_hash
from states import LoginState, RegisterState, AddCarState

# Инициализация всех частей бота

load_dotenv()  # загрузка переменных виртуального окружения
bot = Bot(os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher(storage=MemoryStorage())
init_db()
session = SessionLocal()


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Войти', callback_data='login')],
        [InlineKeyboardButton(text='Зарегистрироваться', callback_data='register')]
    ])
    await message.answer('Здравствуй!', reply_markup=kb)


@dp.callback_query(F.data == 'register')
async def register_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введи своё имя')
    await state.set_state(RegisterState.name)


@dp.message(RegisterState.name)
async def register_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введи свою фамилию (обязательно)')
    await state.set_state(RegisterState.surname)


@dp.message(RegisterState.surname)
async def register_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer('Введи свою почту email (обязательно)')
    await state.set_state(RegisterState.email)


@dp.message(RegisterState.email)
async def register_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer(' Введи свой номер телефона (необязательно)')
    await state.set_state(RegisterState.tel)


@dp.message(RegisterState.tel)
async def register_tel(message: types.Message, state: FSMContext):
    await state.update_data(tel=message.text)
    await message.answer('Введи пароль для твоего аккаунта')
    await state.set_state(RegisterState.password)


@dp.message(RegisterState.password)
async def register_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()

    exist_email = session.query(Users).filter_by(email=data['email']).first()
    exist_tel = session.query(Users).filter_by(tel=data['tel']).first()

    # проверка на существующий мейл и тел
    if exist_email or exist_tel:
        if exist_email:
            await message.answer("Ай-ай-ай! Пользователь с таким email уже имеется!")
        if exist_tel:
            await message.answer("Ай-ай-ай! Пользователь с таким телефоном уже имеется!")
        await state.clear()
        return

    user = Users(
        name=data['name'],
        surname=data['surname'],
        email=data['email'],
        tel=data['tel'],
        password=generate_password_hash(data['password'])
    )

    session.add(user)
    session.commit()  # транзакция

    await message.answer("Пользователь успешно зарегистрирован!")
    await state.clear()

@dp.callback_query(F.data == 'login')
async def login_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введи email')
    await state.set_state(LoginState.email)


@dp.message(LoginState.email)
async def login_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Введи пароль')
    await state.set_state(LoginState.password)


@dp.message(LoginState.password)
async def login_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = session.query(Users).filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, message.text):
        await message.answer("Неверный email или пароль")
        await state.clear()
        return

    session.commit()
    await message.answer(f"Привет, {user.name} {user.surname}", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мои машины", url='https://google.com')],
        [InlineKeyboardButton(text="Добавить машину", callback_data='add_car')],
        [InlineKeyboardButton(text="❌ Выход", url='https://google.com')]
    ]))
    await state.clear()

@dp.callback_query(F.data == 'add_car')
async def add_car_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите государственный регистрационный знак:")
    await state.set_state(AddCarState.plate)

@dp.message(AddCarState.plate)
async def add_car_plate(message: types.Message, state: FSMContext):
    await state.update_data(plate=message.text)
    await message.answer("Введите модель машины:")
    await state.set_state(AddCarState.model)


@dp.message(AddCarState.model)
async def add_car_model(message: types.Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer("Введите цвет машины:")
    await state.set_state(AddCarState.color)


@dp.message(AddCarState.color)
async def add_car_color(message: types.Message, state: FSMContext):
    await state.update_data(color=message.text)
    data = await state.get_data()

    exist_car = session.query(Cars).filter_by(plate=data['plate']).first()
    if exist_car:
        await message.answer("❌ Такая машина уже добавлена")
        await state.clear()
        return

    user = session.query(Users).filter_by(id=2).first()  # поменять на пользователя после логина
    car = Cars(
        plate=data['plate'],
        model=data['model'],
        color=data['color'],
        status=True
    )

    car.users.append(user)
    session.add(car)
    session.commit()
    await message.answer(f"Машина {car.model}, цвет:{car.color}\n"
                         f"c номером: {car.plate} добавлена")
    await state.clear()

async def main():
    await dp.start_polling(bot)

asyncio.run(main())