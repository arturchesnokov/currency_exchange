from bs4 import BeautifulSoup
from celery import shared_task

import requests
from decimal import Decimal

from currency import model_choices as mch
from currency.data_source.service import previous_record_check_and_save, log


@shared_task()
def _otp():
    log.info('OTPBank parser started')
    page = requests.get("https://www.otpbank.com.ua/")
    soup = BeautifulSoup(page.content, 'html.parser')
    currency_bank = soup.find('tbody', class_='currency-list__body')  # <tbody> with bank currency rates
    table_rows = currency_bank.select("tbody tr")  # css selector -> in <tbody> select all <tr>
    # print(table_rows)
    for row in table_rows:
        # print(row)
        currency_name = row.find('td', class_='currency-list__type').text
        if currency_name in {'USD', 'EUR'}:
            currency = {
                'USD': mch.CURR_USD,
                'EUR': mch.CURR_EUR,
            }[currency_name]

            rates = row.findAll('td', class_='currency-list__value')

            rate_kwargs = {
                'currency': currency,
                'buy': round(Decimal(rates[0].text), 2),
                'sale': round(Decimal(rates[1].text), 2),
                'source': mch.SR_OTP,
            }

            previous_record_check_and_save(rate_kwargs)
