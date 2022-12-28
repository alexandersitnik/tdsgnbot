from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot
from datetime import datetime
from register_handlers import admins
import sqlite3

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass

class Registration(StatesGroup):
#класс для регистрации новых пользователей
    id = State()
    Name = State()
    Department = State()
    Grade = State()
    Birthday = State()
    Empoyment = State()
    TelergamID = State()

async def reg_start(message: types.Message):
    await message.answer('Для регистрации введите свой ID')
    await Registration.id.set()

async def reg_id(message: types.Message, state: FSMContext):
    await state.update_data(id=message.text)
    await message.answer('Введите свое имя')
    await Registration.Name.set()

async def reg_name(message: types.Message, state: FSMContext):