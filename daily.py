from datetime import datetime
from aiogram import types, Dispatcher
from create_bot import bot
import sqlite3

superAdmin_ID = 265007461

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass

async def dailyReport():
    today = datetime.today().strftime('%Y-%m-%d')
    today += ' 00:00:00'
    distant_today = c.execute("SELECT Name FROM members WHERE ID IN (SELECT MemberID FROM distant WHERE DistantDate = ?)", (today,)).fetchall()
    distant_today_list = ''
    daily_report = ''
    daily_report = '#ЕжедневныйОтчёт \n' + str(datetime.today().strftime('%d.%m.%Y')) + '\n\n'
    if distant_today != []:
        for el in distant_today:
            distant_today_list += '— ' + str(el[0]) + '\n'
        daily_report += "— Сегодня удалёнка у: \n\n" + str(distant_today_list) + '\n'
    else:
        daily_report += "— Сегодня удалёнки ни у кого нет" + '\n\n'

    sick_today = c.execute("SELECT members.Name, sick.isActive FROM members INNER JOIN sick ON members.ID = sick.MemberID WHERE sick.SickDate = ?", (today,)).fetchall()
    if sick_today != []:
        sick_today_str = ''
        for i in sick_today:
            if i[1] == 1:
                sick_today_str += '— ' + i[0] + ' - работает из дома\n'
            else:
                sick_today_str += '— ' + i[0] + ' - не работает\n'
        daily_report += "\nСегодня болеют:\n\n" + sick_today_str + '\n'
    else:
        daily_report += "\nСегодня никто не болеет\n\n"

    vacations = c.execute("SELECT * FROM vacation WHERE StartVacationDay <= ? AND EndVacationDay >= ?", (datetime.now(), datetime.now())).fetchall()
    todayVacationsAnswer = ''
    if len(vacations) == 0:
        daily_report += "\nСегодня в отпуске никого"
    else:
        for vacation in vacations:
            memberName = c.execute("SELECT Name FROM members WHERE ID = ?", (vacation[0],)).fetchone()[0]
            todayVacationsAnswer += '— ' + memberName + '\n'
            daily_report += "\nСегодня в отпуске:\n\n" + todayVacationsAnswer
    await bot.send_message(-235938403, daily_report)
    await bot.send_message(-1001723462410, daily_report)