from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.dispatcher.filters import Text
import database

class Decesion(StatesGroup):
    lierName = State()
    lierDate = State()
    lierText = State()

# Первый шаг таблицы обмана
async def deception(message: types.Message):
    await Decesion.lierName.set()
    await message.answer("Начинаю процедуру записи обманщика в таблицу 🧐")
    await message.answer("Введи имя лжеца: ")

async def stop_deception(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись ответов отменена")

# Ловим первый ответ
async def deception_lierName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lierName'] = message.text
    await Decesion.next()
    await message.reply("Введи дату обмана в формате дд.мм.гггг: ")

async def deception_lierDate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lierDate'] = message.text
    await Decesion.next()
    await message.reply("Введи текст обмана: ")

async def deception_lierText(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lierText'] = message.text

    await database.sql_add_deception(state)
    await message.reply("Ваше обращение записано, коллега 🫡")
    await state.finish()

async def get_last_deception(message: types.Message):
    await message.answer(database.sql_get_last_deception())

def register_handlers_deception(dp: Dispatcher):
    dp.register_message_handler(deception, commands=['deception'])
    dp.register_message_handler(stop_deception, commands=['stop'], state="*")
    dp.register_message_handler(stop_deception, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(deception_lierName, state=Decesion.lierName)
    dp.register_message_handler(deception_lierDate, state=Decesion.lierDate)
    dp.register_message_handler(deception_lierText, state=Decesion.lierText)
    dp.register_message_handler(get_last_deception, commands=['last_deception'])