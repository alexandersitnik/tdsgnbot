import logging
from aiogram import Bot, Dispatcher, executor, types
from checkpoint import register_handlers_check
from create_bot import dp, Bot
from deseption import register_handlers_deception
from register_handlers import register_handlers

logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    print('Бот запущен')

register_handlers(dp)
register_handlers_check(dp)
register_handlers_deception(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)