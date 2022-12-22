from create_bot import bot, dp
from datetime import datetime
from aiogram import types, Dispatcher
from globals import geshstart, blockstart
#gshtimer
async def geshtimer(message: types.Message):
    geashFate = str(geshstart - datetime.now())
    # geshDays = geashFate.split(' ')[0]
    # geshHours = geashFate.split(' ')[0].split(':')[0]
    # geshMinutes = geashFate.split(' ')[0].split(':')[1]
    # geshSeconds = geashFate.split(' ')[0].split(':')[2].split('.')[0]
    await message.answer('Время Геша настало!')
    await message.answer_sticker(r'CAACAgIAAxkBAAEG8ShjpDnOlUS9-8h45anKXsf8LZCbGwACnwYAAulVBRh_hSfBhR2zUywE')
    # await message.answer('Стартуем в Геш через: \n' + geshHours + ' ч. ' + geshMinutes + ' мин. ' + geshSeconds + ' сек.')

def register_handlers_gesh(dp: Dispatcher):
    dp.register_message_handler(geshtimer, commands=['geshtime'])
