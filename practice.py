import requests
from currency import model_choices as mch
from bs4 import BeautifulSoup

page = requests.get("https://finance.i.ua/")
soup = BeautifulSoup(page.content, 'html.parser')
currency_bank = soup.find('div', class_='widget-currency_bank')  # div with bank currency rates
table_rows = currency_bank.select("div tr")  # css selector -> in <div> select all <tr>
for row in table_rows:
    # print(row)
    if row.find('th'):
        currency_name = row.find('th').text
        if currency_name in {'USD', 'EUR'}:
            print(currency_name)
            rates = row.select('span span')
            print(rates[0].text)
            print(rates[2].text)
            # for rate in rates:
            #     print(rate.text)
