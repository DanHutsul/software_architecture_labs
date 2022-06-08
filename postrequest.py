from urllib import response
import requests

#data = {'msg': 'HELLO'}
url = "http://localhost:8086"

for i in range(10):
    data = {'msg': 'msg' + str(i+1)}
    response = requests.post(url, data)
    print(response.status_code)
    print(response.text)

