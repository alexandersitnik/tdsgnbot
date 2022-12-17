from datetime import datetime
from aiogram import types, Dispatcher
from create_bot import bot
from globals import weekdays_list
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
    week_day = datetime.today().weekday()
    distant_today = c.execute("SELECT Name FROM members WHERE ID IN (SELECT MemberID FROM distant WHERE DistantDate = ?)", (today,)).fetchall()
    distant_today_list = ''
    daily_report = ''
    daily_report = '#ЕжедневныйОтчёт \n' + str(datetime.today().strftime('%d.%m.%Y')) + ', ' + str(weekdays_list[week_day])+ '\n\n'
    if distant_today != []:
        for el in distant_today:
            distant_today_list += '— ' + str(el[0]) + '\n'
        daily_report += "*Сегодня удалёнка у:* \n" + str(distant_today_list) + '\n'
    else:
        daily_report += "*Сегодня удалёнки ни у кого нет*" + '\n\n'

    sick_today = c.execute("SELECT members.Name, sick.isActive FROM members INNER JOIN sick ON members.ID = sick.MemberID WHERE sick.SickDate = ?", (today,)).fetchall()
    if sick_today != []:
        sick_today_str = ''
        for i in sick_today:
            if i[1] == 1:
                sick_today_str += '— ' + i[0] + ' - работает из дома\n'
            else:
                sick_today_str += '— ' + i[0] + ' - не работает\n'
        daily_report += "\n*Сегодня болеют:*\n" + sick_today_str + '\n'
    else:
        daily_report += "\n*Сегодня никто не болеет*\n\n"

    todaydate = datetime.now()
    todaydate= todaydate.replace(hour=0, minute=0, second=0, microsecond=0)
    vacations = c.execute("SELECT * FROM vacation WHERE StartVacationDay <= ? AND EndVacationDay >= ?", (todaydate, todaydate)).fetchall()
    todayVacationsAnswer = ''
    if len(vacations) == 0:
        daily_report += "\n*Сегодня в отпуске никого*"
    else:
        daily_report += "\n*Сегодня в отпуске*:\n" 
        for vacation in vacations:
            memberName = c.execute("SELECT Name FROM members WHERE ID = ?", (vacation[0],)).fetchone()[0]
            todayVacationsAnswer += '— ' + memberName + '\n'
        daily_report += todayVacationsAnswer
    if week_day <5:
        await bot.send_message(-235938403, daily_report, parse_mode='Markdown')
        await bot.send_message(-1001723462410, daily_report, parse_mode='Markdown')
    else:
        await bot.send_message(superAdmin_ID, 'Сегодня выходной, отчёт не отправлен')