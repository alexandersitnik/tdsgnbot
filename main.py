import logging
from aiogram import Bot, Dispatcher, executor, types
from create_bot import dp, Bot
from register_handlers import register_handlers

logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    print('Bot is online!')

register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)