from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from datetime import datetime
from register_handlers import translators, admins
import sqlite3

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass

class Vacations(StatesGroup):
    vacationMember = State()
    vacationMemberStartDate = State()
    vacationMemberEndDate = State()
    vacationIsPaid = State()

async def vacation(message: types.Message, state: FSMContext):
    if (message.chat.type == 'private'):
        await Vacations.vacationMember.set()
        memberName = c.execute("SELECT Name FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
        await message.answer("Начинаю процедуру записи отпуска 🧐\n\nТы идентифицирован как: " + memberName + ".\n\n Если это не ты или просто хочешь остановить запись, то напиши /stop или «отмена»")
        async with state.proxy() as data:
            data['vacationMember'] = c.execute("SELECT ID FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
        await Vacations.next()
        await message.answer("Введи дату отпуска в формате ДД.ММ.ГГГГ")
    else:
        await message.answer("Команда доступна только в личных сообщениях")

async def stop_vacation(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Запись ответов отменена")

async def vacationMemberStartDate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        formated_date = ''
        try:
            formated_date = datetime.strptime(message.text, '%d.%m.%Y')
        except:
            await message.answer("Неверный формат даты. Попробуй ещё раз")
            return
        data['vacationMemberStartDate'] = formated_date
        await message.answer("Введи дату окончания отпуска в формате ДД.ММ.ГГГГ")
        await Vacations.next()

async def vacationMemberEndDate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        formated_date = ''
        try:
            formated_date = datetime.strptime(message.text, '%d.%m.%Y')
        except:
            await message.answer("Неверный формат даты. Попробуй ещё раз")
            return
        data['vacationMemberEndDate'] = formated_date
        await message.answer("Отпуск оплачивается? (Да/Нет)")
        await Vacations.next()

async def vacationIsPaid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == 'да':
            data['vacationIsPaid'] = 1
        elif message.text.lower() == 'нет':
            data['vacationIsPaid'] = 0
        else:
            await message.answer("Неверный ответ. Попробуй ещё раз")
            return
        #записать полученные значения в базу данных
        c.execute("INSERT INTO vacation (MemberID, StartVacationDay, EndVacationDay, isPaid) VALUES (?, ?, ?, ?)", (data['vacationMember'], data['vacationMemberStartDate'], data['vacationMemberEndDate'], data['vacationIsPaid']))
        db.commit()
        await message.answer("Отпуск успешно записан")
        for el in admins:
            await message.bot.send_message(el, "#отпуски\n\n Новый отпуск у: \n" + c.execute("SELECT Name FROM members WHERE ID = ?", (data['vacationMember'],)).fetchone()[0] + " записал отпуск с " + data['vacationMemberStartDate'].strftime('%d.%m.%Y') + " по " + data['vacationMemberEndDate'].strftime('%d.%m.%Y') + ".\n\nОплачивается: " + ("Да" if data['vacationIsPaid'] == 1 else "Нет"))
        await state.finish()

#----------------------------Выводы в клиентскую часть----------------------------------------------------

# вывести все мои отпуски в текущем году
async def my_vacations(message: types.Message, state: FSMContext):
    totalDays = 0
    i = 1
    myVacationsAnswer = 'Вот твои отпуска в текущем году:\n\n'
    memberID = c.execute("SELECT ID FROM members WHERE TelegramID = ?", (message.from_user.id,)).fetchone()[0]
    vacations = c.execute("SELECT * FROM vacation WHERE MemberID = ? AND StartVacationDay BETWEEN ? AND ?", (memberID, datetime(datetime.now().year, 1, 1), datetime(datetime.now().year, 12, 31))).fetchall()
    if len(vacations) == 0:
        await message.answer("У тебя нет отпусков в текущем году")
        return
    else:
        for vacation in vacations:
            myVacationsAnswer += "Отпуск № " + str(i) + '\n' + ' c ' +str(vacation[1].split()[0]) + " по " + str(vacation[2].split()[0]) + '\n'
            #привести vacation[1] и vacation[2] которые на данный момент являются строкой к типу datetime
            dayTwo = vacation[2]
            dayTwo = datetime.strptime(dayTwo, '%Y-%m-%d %H:%M:%S')
            dayOne = vacation[1]
            dayOne = datetime.strptime(dayOne, '%Y-%m-%d %H:%M:%S')
            countOfVacationDays = dayTwo - dayOne
            totalDays += int(countOfVacationDays.days)
            i += 1
        myVacationsAnswer += "\nОсталось дней в этом году: " + str(28-totalDays)
        await message.answer(myVacationsAnswer)

# вывести есть ли на сегодня у кого-то отпуск
async def today_vacations(message: types.Message):
    todayVacationsAnswer = 'Сегодня в отпуске:\n\n'
    todaydate = datetime.now()
    todaydate= todaydate.replace(hour=0, minute=0, second=0, microsecond=0)
    vacations = c.execute("SELECT * FROM vacation WHERE StartVacationDay <= ? AND EndVacationDay >= ?", (todaydate, todaydate)).fetchall()
    if len(vacations) == 0:
        await message.answer("*В отпуске никого*", parse_mode= 'Markdown')
        return
    else:
        for vacation in vacations:
            memberName = c.execute("SELECT Name FROM members WHERE ID = ?", (vacation[0],)).fetchone()[0]
            todayVacationsAnswer += memberName + '\n'
        await message.answer(todayVacationsAnswer)
        


def register_handlers_vacation(dp: Dispatcher):
    dp.register_message_handler(vacation, commands="vacation", state="*")
    dp.register_message_handler(stop_vacation, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(vacationMemberStartDate, state=Vacations.vacationMemberStartDate)
    dp.register_message_handler(vacationMemberEndDate, state=Vacations.vacationMemberEndDate)
    dp.register_message_handler(vacationIsPaid, state=Vacations.vacationIsPaid)
    dp.register_message_handler(my_vacations, commands="my_vacations")
    dp.register_message_handler(today_vacations, commands="today_vacations")