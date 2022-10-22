from aiogram import types, Dispatcher
from database import format_members

# @dp.message_handler(commands=['start', 'help'])
async def send_message(message: types.Message):
    await message.answer("Hello! I'm EchoBot!\nPowered by aiogram.")
async def send_members(message: types.Message):
    format_members()
    await message.answer("Members: " + format_members())

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(send_message, commands=['start', 'help'])
    dp.register_message_handler(send_members, commands = ['members'])