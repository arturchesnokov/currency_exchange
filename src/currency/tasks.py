from celery import shared_task
import requests
from decimal import Decimal, getcontext
from monobank_api import BaseAPI

from currency.models import Rate

from currency import model_choices as mch


# check previous record with currency and source, if currency rate changed - save it
def previous_record_check_and_save(rate_kwargs):
    new_rate = Rate(**rate_kwargs)

    last_rate = Rate.objects.filter(currency=new_rate.currency, source=new_rate.source).last()

    if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
        new_rate.save()


def _privat():
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
    mono = BaseAPI()
    currencies = mono.get_currency()

    for rate in currencies:
        if int(rate['currencyCodeB']) == 980 and (int(rate['currencyCodeA']) in {840, 978, }):
            print(rate)

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


@shared_task()
def parse_rates():
    _privat()
    _mono()
