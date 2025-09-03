import asyncio
#from tkinter.tix import ResizeHandle

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


TOKEN = "8401965285:AAGgguWlbPOKzToFR3Gp_wKN9lXDZIDPeiA"
bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class RegisterState(StatesGroup): # регистрация
    name = State()
    surname = State()
    email = State()
    tel = State()
    password = State()


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Войти', url='google.com')], [InlineKeyboardButton(text='Зарегистрироваться', callback_data='register')]])
    await message.answer('Здравствуй!', reply_markup=kb)

@dp.callback_query(F.data=='register')
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


async def main():
    await dp.start_polling(bot)

asyncio.run(main())