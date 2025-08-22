import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "8401965285:AAGgguWlbPOKzToFR3Gp_wKN9lXDZIDPeiA"
bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Войти')], [InlineKeyboardButton(text='')]])
    await message.answer(f"Здравствуй!")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())