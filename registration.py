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


class UserRegistration(StatesGroup):
    confirm = None
    name = State()
    department = State()
    grade = State()
    birthday = State()
    employment = State()


async def start_registration (message: types.Message):
    await message.answer(
        "Начинаю процедуру регистрации 🧐\n\nЕсли хочешь остановить запись, то напиши /stop или «отмена»")
    await message.answer("Введи своё имя")
    await UserRegistration.name.set()


async def stop_registration (message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись ответов отменена")


async def name (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await message.answer("Введи свой отдел")
        await UserRegistration.next()


async def department (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['department'] = message.text
        await message.answer("Введи свой уровень")
        await UserRegistration.next()


async def grade (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['grade'] = message.text
        await message.answer("Введи свою дату рождения в формате ДД.ММ.ГГГГ")
        await UserRegistration.next()


async def birthday (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        formated_date = ''
        try:
            formated_date = datetime.strptime(message.text, '%d.%m.%Y')
        except:
            await message.answer("Неверный формат даты. Попробуй ещё раз")
            return
        data['birthday'] = formated_date
        await message.answer("Введи дату начала работы в формате ДД.ММ.ГГГГ")
        await UserRegistration.next()


async def employment (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        formated_date = ''
        try:
            formated_date = datetime.strptime(message.text, '%d.%m.%Y')
        except:
            await message.answer("Неверный формат даты. Попробуй ещё раз")
            return
        data['employment'] = formated_date
        await message.answer(
            "Всё верно?\n\nИмя: " + data['name'] + "\nОтдел: " + data['department'] + "\nУровень: " + data[
                'grade'] + "\nДата рождения: " + data['birthday'].strftime('%d.%m.%Y') + "\nДата начала работы: " +
            data['employment'].strftime('%d.%m.%Y') + "\n\nЕсли всё верно, то напиши «да» или «нет»")
        await UserRegistration.next()


async def confirm (message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == 'да':
            c = sqlite3.connect('users.db')
            c.execute("INSERT INTO members (Name, Department, Grade, Birthday, Employment) VALUES (?, ?, ?, ?, ?)",
                      (data['name'], data['department'], data['grade'], data['birthday'], data['employment']))
            c.commit()
            await message.answer("Регистрация прошла успешно")
            await state.finish()
        elif message.text.lower() == 'нет':
            await message.answer("Запись ответов отменена")
            await state.finish()
        else:
            await message.answer("Неверный ответ. Попробуй ещё раз")
            return


def register_handlers_registration (dp: Dispatcher):
    dp.register_message_handler(start_registration, commands="registration", state="*")
    dp.register_message_handler(stop_registration, commands="stop", state="*")
    dp.register_message_handler(name, state=UserRegistration.name)
    dp.register_message_handler(department, state=UserRegistration.department)
    dp.register_message_handler(grade, state=UserRegistration.grade)
    dp.register_message_handler(birthday, state=UserRegistration.birthday)
    dp.register_message_handler(employment, state=UserRegistration.employment)
    dp.register_message_handler(confirm, state=UserRegistration.confirm)
