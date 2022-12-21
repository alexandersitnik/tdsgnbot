import logging
import asyncio
from async_scheduler import AsyncScheduler, Job, Periods
from aiogram import Bot, Dispatcher, executor, types
from calendar_1 import register_handlers_calendar
from create_bot import bot
from checkpoint import register_handlers_check
from create_bot import dp, Bot
from daily import dailyReport
from deseption import register_handlers_deception
from fortest import register_handlers_ny
from geshtimer import register_handlers_gesh
from register_handlers import register_handlers
from keyboards.registration_kb import register_handlers_members_kb
from distant import register_handlers_distant, distant_today_personal
from sick import register_handlers_sick
from vacation import register_handlers_vacation
from hookahtimer import register_handlers_hookah
from echo import register_handlers_inline

scheduler = AsyncScheduler([])

async def send_test():
    await bot.send_message(265007461, text='Тестовое сообщение')


logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    print('Бот запущен')
register_handlers(dp)
register_handlers_check(dp)
register_handlers_deception(dp)
register_handlers_members_kb(dp)
register_handlers_distant(dp)
register_handlers_vacation(dp)
register_handlers_sick(dp)
register_handlers_inline(dp)
register_handlers_gesh(dp)
register_handlers_hookah(dp)
register_handlers_calendar(dp)
register_handlers_ny(dp)
if __name__ == '__main__':
    scheduler.add_to_loop()
    scheduler.add_job(Job('send_daily', dailyReport, None, Periods.minute, 1440, '22.12.22 11:30'))
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)