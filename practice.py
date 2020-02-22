import requests
from currency import model_choices as mch
from bs4 import BeautifulSoup

url = 'https://obmen.dp.ua/controls'
data = {"getrates": "true"}
response = requests.post(url, data)
assert response.status_code == 200
r_json = response.json()['data']['rates']
print(r_json)


