from create_bot import bot, dp
from datetime import datetime
from aiogram import types, Dispatcher
from globals import geshstart, blockstart
#gshtimer
async def geshtimer(message: types.Message):
    geashFate = str(geshstart - datetime.now())
    geshDays = geashFate.split(' ')[0]
    geshHours = geashFate.split(' ')[2].split(':')[0]
    geshMinutes = geashFate.split(' ')[2].split(':')[1]
    geshSeconds = geashFate.split(' ')[2].split(':')[2].split('.')[0]
    await message.answer('Стартуем в Геш через: \n' + geshDays + ' д. ' + geshHours + ' ч. ' + geshMinutes + ' мин. ' + geshSeconds + ' сек.')

async def blockchat(message: types.Message):
    chatFate = str(datetime.now() - blockstart)
    print(chatFate)
    chatDays = chatFate.split(' ')[0]
    chatHours = chatFate.split(' ')[2].split(':')[0]
    chatMinutes = chatFate.split(' ')[2].split(':')[1]
    chatSeconds = chatFate.split(' ')[2].split(':')[2].split('.')[0]
    await message.answer('Чатоблокада длится уже: \n' + chatDays + ' д. ' + chatHours + ' ч. ' + chatMinutes + ' мин. ' + chatSeconds + ' сек.')

def register_handlers_gesh(dp: Dispatcher):
    dp.register_message_handler(geshtimer, commands=['geshtime'])
    dp.register_message_handler(blockchat, commands=['blocktime'])
