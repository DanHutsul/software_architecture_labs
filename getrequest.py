from urllib import response
import requests

data = {'msg': 'HELLO'}
url = "http://localhost:8086"

response = requests.get(url, data)
print(response.status_code)
print(response.text)

