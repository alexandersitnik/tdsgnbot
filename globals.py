from datetime import datetime

geshstart = datetime.strptime('22.12.2023', "%d.%m.%Y")
geshstart = geshstart.replace(hour=19, minute=0, second=0, microsecond=0)

blockstart = datetime.strptime('06.12.2022', "%d.%m.%Y")
blockstart = blockstart.replace(hour=10, minute=8, second=0, microsecond=0)

weekdays_list = ['понедельник', 'вторник','среда','четверг','пятница','суббота','воскресенье']
print(blockstart)
print(weekdays_list[0])
