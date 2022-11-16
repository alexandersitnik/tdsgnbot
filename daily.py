from datetime import datetime
from aiogram import types, Dispatcher
import sqlite3

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass
# сегодняняя удалёнка
async def dailyReport(message: types.Message):
    today = datetime.today().strftime('%Y-%m-%d')
    today += ' 00:00:00'
    distant_today = c.execute("SELECT Name FROM members WHERE ID IN (SELECT MemberID FROM distant WHERE DistantDate = ?)", (today,)).fetchall()
    distant_today_list = ''
    if distant_today != []:
        for el in distant_today:
            distant_today_list += '📌 ' + str(el[0]) + '\n'
        await message.answer("🏠 Сегодня удалёнка у: \n\n" + str(distant_today_list))
    else:
        await message.answer("Сегодня удалёнок ни у кого нет")
# сегодняшние отпуска
    todayVacationsAnswer = 'Сегодня в отпуске:\n\n'
    vacations = c.execute("SELECT * FROM vacation WHERE StartVacationDay <= ? AND EndVacationDay >= ?", (datetime.now(), datetime.now())).fetchall()
    if len(vacations) == 0:
        await message.answer("В отпуске никого")
        return
    else:
        for vacation in vacations:
            memberName = c.execute("SELECT Name FROM members WHERE ID = ?", (vacation[0],)).fetchone()[0]
            todayVacationsAnswer += memberName + '\n'
        await message.answer(todayVacationsAnswer)

def register_handlers_daily(dp : Dispatcher):
    dp.register_message_handler(dailyReport, commands = ['daily'])