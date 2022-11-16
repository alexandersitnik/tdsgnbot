import datetime

#записать в переменную сегодняшнюю дату и время 00:00:00
today = datetime.datetime.today().strftime('%Y-%m-%d 00:00:00')
print(today)
