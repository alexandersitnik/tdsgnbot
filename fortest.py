import requests
import json

url = "https://zeapi.yandex.net/lab/api/yalm/text3"

payload = json.dumps({
  "filter": 1,
  "into": 0,
  "query": "Тест был"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)