from aiogram import types, Dispatcher

# @dp.message_handler(commands=['start', 'help'])
async def send_message(message: types.Message):
    await message.answer("Hello! I'm EchoBot!\nPowered by aiogram.")

def register_handlers(dp : Dispatcher):
    dp.register_message_handler(send_message, commands=['start', 'help'])