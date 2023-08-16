from datetime import datetime, timedelta
from aiogram import types, Dispatcher
from create_bot import bot
from globals import weekdays_list
import sqlite3, requests

superAdmin_ID = 265007461

try:
    db = sqlite3.connect('./data/tdsgnBotBase.db')
    c = db.cursor()
except:
    pass

async def tomorrowReport():
    today = datetime.today().strftime('%Y-%m-%d')
    today += ' 00:00:00'
    tomorrow = datetime.today() + timedelta(days=1)
    tomorrow_str = datetime.today() + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    tomorrow += ' 00:00:00'

    week_day = datetime.today().weekday() + 1

    distant_today = c.execute("SELECT Name FROM members WHERE ID IN (SELECT MemberID FROM distant WHERE DistantDate = ?)", (tomorrow,)).fetchall()
    distant_today_list = ''
    daily_report = ''
    daily_report = '#ВечернийОтчёт \n' + 'Завтра: ' + str(tomorrow_str.strftime('%d.%m.%Y')) + ', ' + str(weekdays_list[week_day])+ '\n\n'
    if distant_today != []:
        for el in distant_today:
            distant_today_list += '— ' + str(el[0]) + '\n'
        daily_report += "*Завтра на удалёнке:* \n" + str(distant_today_list) + '\n'
    else:
        daily_report += "*Завтра удалёнки ни у кого нет*" + '\n\n'

    sick_today = c.execute("SELECT members.Name, sick.isActive FROM members INNER JOIN sick ON members.ID = sick.MemberID WHERE sick.SickDate = ?", (tomorrow,)).fetchall()
    if sick_today != []:
        sick_today_str = ''
        for i in sick_today:
            if i[1] == 1:
                sick_today_str += '— ' + i[0] + ' - работает из дома\n'
            else:
                sick_today_str += '— ' + i[0] + ' - не работает\n'
        daily_report += "\n*Завтра болеют:*\n" + sick_today_str + '\n'
    else:
        daily_report += "\n*Завтра никто не болеет*\n\n"

    todaydate = datetime.today() + timedelta(days=1)
    todaydate= todaydate.replace(hour=0, minute=0, second=0, microsecond=0)
    vacations = c.execute("SELECT * FROM vacation WHERE StartVacationDay <= ? AND EndVacationDay >= ?", (todaydate, todaydate)).fetchall()
    todayVacationsAnswer = ''
    if len(vacations) == 0:
        daily_report += "\n*Завтра в отпуске никого*"
    else:
        daily_report += "\n*Завтра в отпуске*:\n"
        for vacation in vacations:
            memberName = c.execute("SELECT Name FROM members WHERE ID = ?", (vacation[0],)).fetchone()[0]
            todayVacationsAnswer += '— ' + memberName + '\n'
        daily_report += todayVacationsAnswer
    # async def get_weather(city_name):
    #     # weather_url = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid=05a9fb1cecaca7a61f846213566c28f9"
    #     #weather_url = "https://wttr.in/{}?0&m&T&q&lang=ru".format(city_name)
    #     weather_url = "https://wttr.in/{}?m&format=2&lang=ru".format(city_name)
    #     response = requests.get(weather_url)
    #     return response.text
    # weather = await get_weather('Новосибирск')
    # daily_report += '\n\n Температура в Томске:\n' + str(weather)
    if week_day <5:
        await bot.send_message(-235938403, daily_report, parse_mode='Markdown')
        await bot.send_message(-1001723462410, daily_report, parse_mode='Markdown')
        # await bot.send_message(265007461, daily_report, parse_mode='Markdown')
    else:
        await bot.send_message(superAdmin_ID, 'Сегодня выходной, отчёт не отправлен')