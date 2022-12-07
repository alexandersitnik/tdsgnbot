from datetime import datetime

blockstart = datetime.strptime('06.12.2022', "%d.%m.%Y")
blockstart = blockstart.replace(hour=16, minute=6, second=0, microsecond=0)

print(datetime.now() - blockstart)