from celery import shared_task
import requests
import logging
from decimal import Decimal
from bs4 import BeautifulSoup

from monobank_api import BaseAPI

from currency.models import Rate

from currency import model_choices as mch

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("parser")


# check previous record with currency and source, if currency rate changed - save it
def previous_record_check_and_save(rate_kwargs):
    new_rate = Rate(**rate_kwargs)  # create new instance of currency record

    # get last currency record for source
    last_rate = Rate.objects.filter(currency=new_rate.currency, source=new_rate.source).last()

    # verify and save if records are different
    if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
        new_rate.save()


def _privat():
    log.info('PrivatBank parser started')
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    r_json = response.json()

    for rate in r_json:
        if rate['ccy'] in {'USD', 'EUR'}:
            currency = mch.CURR_USD if rate['ccy'] == 'USD' else mch.CURR_EUR

            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(rate['buy']),
                'sale': Decimal(rate['sale']),
                'source': mch.SR_PRIVAT,
            }
            previous_record_check_and_save(rate_kwargs)


# 980 UAH
# 978 EUR
# 840 USD
def _mono():
    log.info('MonoBank parser started')
    mono = BaseAPI()
    currencies = mono.get_currency()

    for rate in currencies:
        if int(rate['currencyCodeB']) == 980 and (int(rate['currencyCodeA']) in {840, 978, }):
            currency = {
                840: mch.CURR_USD,
                978: mch.CURR_EUR,
            }[int(rate['currencyCodeA'])]

            rate_kwargs = {
                'currency': currency,
                'buy': round(Decimal(rate['rateBuy']), 2),
                'sale': round(Decimal(rate['rateSell']), 2),
                'source': mch.SR_MONO,
            }

            previous_record_check_and_save(rate_kwargs)


def _vkurse_dp_ua():
    log.info('vkurse.dp.ua parser started')
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    assert response.status_code == 200
    r_json = response.json()

    for currency_name, value in r_json.items():
        if currency_name in {'Dollar', 'Euro'}:
            currency = {
                'Dollar': mch.CURR_USD,
                'Euro': mch.CURR_EUR,
            }[currency_name]

            rate_kwargs = {
                'currency': currency,
                'buy': round(Decimal(value['buy']), 2),
                'sale': round(Decimal(value['sale']), 2),
                'source': mch.SR_VKURSE_DP,
            }

            previous_record_check_and_save(rate_kwargs)


def _obmen_dp_ua():
    log.info('obmen.dp.ua parser started')
    url = 'https://obmen.dp.ua/controls'
    data = {"getrates": "true"}
    response = requests.post(url, data)
    assert response.status_code == 200
    r_json = response.json()['data']['rates']

    for rate in r_json:
        if rate['alias'] in {'usd-uah', 'eur-uah'}:
            currency = {
                'USD': mch.CURR_USD,
                'EUR': mch.CURR_EUR,
            }[rate['currencyBase']]

            rate_kwargs = {
                'currency': currency,
                'buy': round(Decimal(rate['rateBid']), 2),
                'sale': round(Decimal(rate['rateAsk']), 2),
                'source': mch.SR_OBMEN_DP,
            }

            previous_record_check_and_save(rate_kwargs)


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

                rates = row.select('span span') # spans inside spans

                rate_kwargs = {
                    'currency': currency,
                    'buy': round(Decimal(rates[0].text), 2),
                    'sale': round(Decimal(rates[2].text), 2),
                    'source': mch.SR_FINANCE_I_UA,
                }

                previous_record_check_and_save(rate_kwargs)


@shared_task()
def parse_rates():
    _privat()
    _mono()
    _vkurse_dp_ua()
    _obmen_dp_ua()
    _finance_i_ua()
