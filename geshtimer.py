from create_bot import bot, dp
from datetime import datetime
from aiogram import types, Dispatcher
from globals import geshstart
#gshtimer
async def geshtimer(message: types.Message):
    geashFate = str(geshstart - datetime.now())
    geshDays = geashFate.split(' ')[0]
    geshHours = geashFate.split(' ')[2].split(':')[0]
    geshMinutes = geashFate.split(' ')[2].split(':')[1]
    geshSeconds = geashFate.split(' ')[2].split(':')[2].split('.')[0]
    await message.answer('Стартуем в Геш через: \n' + geshDays + ' дней ' + geshHours + ' часов ' + geshMinutes + ' минут ' + geshSeconds + ' секунд')

def register_handlers_gesh(dp: Dispatcher):
    dp.register_message_handler(geshtimer, commands=['geshtime'])
