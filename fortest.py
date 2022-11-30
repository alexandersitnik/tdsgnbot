
from datetime import datetime
d = datetime.now()
#установить время в переменной d на 00 00 00
d = d.replace(hour=0, minute=0, second=0, microsecond=0)
day = d.weekday()
print(d)
print(day)