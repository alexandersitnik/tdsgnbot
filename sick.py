from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import bot
from datetime import datetime
from register_handlers import admins, translators
import sqlite3

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass

class Sick(StatesGroup):
    MemberID = State()
    SickDate = State()
    isActive = State()

async def sick(message: types.Message, state: FSMContext):
    await Sick.MemberID.set()
    memberName = c.execute("SELECT Name FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
    await message.answer("Начинаю процедуру записи больничного 🤒\n\nТы идентифицирован как: " + memberName + ".\n\n Если это не ты или просто хочешь остановить запись, то напиши /stop или «отмена»")
    async with state.proxy() as data:
        data['MemberID'] = c.execute("SELECT ID FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
    await Sick.next()
    await message.answer("Введи дату начала больничного в формате ДД.ММ.ГГГГ")

async def stop_sick(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись ответов отменена")

async def sick_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        fromated_date = ''
        try:
            fromated_date = datetime.strptime(message.text, '%d.%m.%Y')
        except:
            await message.answer("Неверный формат даты. Попробуй еще раз")
            return
        data['SickDate'] = fromated_date
    await message.answer('А работать будешь из дома? (да/нет)')
    await Sick.next()

async def sick_is_active(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == 'да':
            data['isActive'] = 1
        elif message.text.lower() == 'нет':
            data['isActive'] = 0
        else:
            await message.answer("Неверный ответ. Попробуй еще раз")
            return
    try:
        c.execute("INSERT INTO sick (MemberID, SickDate, isActive) VALUES (?, ?, ?)", (data['MemberID'], data['SickDate'], data['isActive']))
        db.commit()
        await message.answer("Запись больничного прошла успешно\n Поправляйся☀️\n\n Если вечером поймешь, что завтра не выйдешь на работу, то заполни еще один день /sick. Да-да и так каждый день, что поделать 🤷‍♂️")
        for el in admins:
            await bot.send_message(el, "#больничные\n\n Дата: " + str(data['SickDate'].split(" ")[0]) + "\n" + "Кто: " + c.execute("SELECT Name FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0] + "\n" + "Будет работать из дома: " + str(data['isActive']) + "\n\n P.S. 1 - работает из дома, 0 - нет")
        await state.finish()
    except:
        await message.answer("Что-то пошло не так. Попробуй еще раз. Возможно ты уже записал больничный на эту дату, попробуй команду: /who_is_sick_today")
        await state.finish()

#выводы в клиентскую часть

async def who_is_sick_today(message: types.Message):
    today = datetime.today().strftime('%Y-%m-%d 00:00:00')
    #выбрать всех кто сегодня болеет, записать в строку с перносом строки их имена и стаус (работает из дома или нет)
    sick_today = c.execute("SELECT members.Name, sick.isActive FROM members INNER JOIN sick ON members.ID = sick.MemberID WHERE sick.SickDate = ?", (today,)).fetchall()
    if sick_today:
        sick_today_str = ''
        for i in sick_today:
            if i[1] == 1:
                sick_today_str += i[0] + ' - работает из дома\n'
            else:
                sick_today_str += i[0] + ' - не работает\n'
        await message.answer("Сегодня болеют:\n" + sick_today_str)
    else:
        await message.answer("Сегодня никто не болеет")



def register_handlers_sick(dp: Dispatcher):
    dp.register_message_handler(sick, Text(equals="/sick"), state="*")
    dp.register_message_handler(stop_sick, Text(equals="/stop"), state="*")
    dp.register_message_handler(stop_sick, Text(equals="отмена"), state="*")
    dp.register_message_handler(sick_date, state=Sick.SickDate)
    dp.register_message_handler(sick_is_active, state=Sick.isActive)
    dp.register_message_handler(who_is_sick_today, Text(equals="/who_is_sick_today"))