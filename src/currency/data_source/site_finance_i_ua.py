from bs4 import BeautifulSoup

import requests
from decimal import Decimal

from currency import model_choices as mch
from currency.data_source.service import previous_record_check_and_save, log


def _finance_i_ua():
    log.info('finance.i.ua parser started')
    page = requests.get("https://finance.i.ua/")
    soup = BeautifulSoup(page.content, 'html.parser')
    currency_bank = soup.find('div', class_='widget-currency_bank')  # div with bank currency rates
    table_rows = currency_bank.select("div tr")  # css selector -> in <div> select all <tr>
    for row in table_rows:
        if row.find('th'):
            currency_name = row.find('th').text
            if currency_name in {'USD', 'EUR'}:
                currency = {
                    'USD': mch.CURR_USD,
                    'EUR': mch.CURR_EUR,
                }[currency_name]

                rates = row.select('span span')  # spans inside spans

                rate_kwargs = {
                    'currency': currency,
                    'buy': round(Decimal(rates[0].text), 2),
                    'sale': round(Decimal(rates[2].text), 2),
                    'source': mch.SR_FINANCE_I_UA,
                }

                previous_record_check_and_save(rate_kwargs)
