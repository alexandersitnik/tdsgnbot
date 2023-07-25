from calendar import monthrange
import calendar
import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot
from datetime import datetime, timedelta
from register_handlers import admins
import sqlite3

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass


class Ssl(StatesGroup):
    sslName = State()
    sslStartDate = State()
    sslEndDate = State()
    sslIsPaid = State()


async def add_new_ssl (message: types.Message, state: FSMContext):
    if (message.from_user.id in admins):
        await message.answer(
            "Начинаю процедуру добавления нового SSL сертификата 🧐\n\nЕсли хочешь остановить запись, то напиши /stop или «отмена»")
        await message.answer("Введи название проекта, для которого добавляем SSL")
        await Ssl.sslName.set()
    else:
        await message.answer("Команда доступна только администраторам")


async def stop_ssl (message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись ответов отменена")


async def sslName (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sslName'] = message.text
        await message.answer("Введи дату начала действия сертификата в формате ДД.ММ.ГГГГ")
        await Ssl.next()


async def sslStartDate (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        formated_date = ''
        try:
            formated_date = datetime.strptime(message.text, '%d.%m.%Y')
        except:
            await message.answer("Неверный формат даты. Попробуй ещё раз")
            return
        data['sslStartDate'] = formated_date
        await message.answer("Введи дату окончания действия сертификата в формате ДД.ММ.ГГГГ")
        await Ssl.next()


async def sslEndDate (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        formated_date = ''
        try:
            formated_date = datetime.strptime(message.text, '%d.%m.%Y')
        except:
            await message.answer("Неверный формат даты. Попробуй ещё раз")
            return
        data['sslEndDate'] = formated_date
        await message.answer("Сертик платный?")
        await Ssl.next()


async def sslIsPaid (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sslIsPaid'] = message.text
        try:
            c.execute("INSERT INTO SSL VALUES (?, ?, ?, ?)",
                      (data['sslName'], data['sslStartDate'], data['sslEndDate'], data['sslIsPaid']))
            db.commit()
            await message.answer("Сертификат добавлен в базу данных")
            await state.finish()
        except:
            await message.answer("Произошла ошибка при добавлении сертификата в базу данных")
            return


async def get_ssl_table (message: types.Message):
    if (message.chat.type == 'private' and message.from_user.id in admins):
        ssl_table = c.execute("SELECT * FROM SSL").fetchall()
        await message.answer("Таблица SSL сертификатов:")
        for row in ssl_table:
            await message.answer(f"Название: {row[0]}\nДата начала: {row[1]}\nДата окончания: {row[2]}\nПлатный: {row[3]}")
    else:
        await message.answer("Команда доступна только администраторам")

def register_handlers_ssl (dp: Dispatcher):
    dp.register_message_handler(add_new_ssl, commands=['add_ssl'])
    dp.register_message_handler(stop_ssl, commands=['stop'], state="*")
    dp.register_message_handler(sslName, state=Ssl.sslName)
    dp.register_message_handler(sslStartDate, state=Ssl.sslStartDate)
    dp.register_message_handler(sslEndDate, state=Ssl.sslEndDate)
    dp.register_message_handler(sslIsPaid, state=Ssl.sslIsPaid)
    dp.register_message_handler(get_ssl_table, commands=['get_ssl_table'])
