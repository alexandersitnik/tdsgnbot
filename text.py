import requests

access_key = '08n8jA9QSZqQWUEgpD6x98jcPR5BxpDG'
url = 'http://apilayer.net/api/live?access_key=' + access_key + '&currencies=RUB&source=USD&format=1'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    usd_to_rub_rate = data['quotes']['USDRUB']
    print('Курс доллара к рублю: ', usd_to_rub_rate)
else:
    print('Произошла ошибка при получении данных:', response.status_code)
