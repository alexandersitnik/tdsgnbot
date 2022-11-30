from datetime import datetime

geshstart = datetime.strptime('22.12.2022', "%d.%m.%Y")
geshstart = geshstart.replace(hour=19, minute=0, second=0, microsecond=0)

weekdays_list = ['понедельник', 'вторник','среда','четверг','пятница','суббота','воскресенье']
print(geshstart)
print(weekdays_list[0])
