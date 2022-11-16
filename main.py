import logging
from aiogram import Bot, Dispatcher, executor, types
from checkpoint import register_handlers_check
from create_bot import dp, Bot
from daily import register_handlers_daily
from deseption import register_handlers_deception
from register_handlers import register_handlers
from keyboards.registration_kb import register_handlers_members_kb
from distant import register_handlers_distant
from sick import register_handlers_sick
from vacation import register_handlers_vacation

logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    print('Бот запущен')
#комментарий
register_handlers(dp)
register_handlers_check(dp)
register_handlers_deception(dp)
register_handlers_members_kb(dp)
register_handlers_distant(dp)
register_handlers_vacation(dp)
register_handlers_daily(dp)
register_handlers_sick(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)