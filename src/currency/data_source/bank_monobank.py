from monobank_api import BaseAPI
from celery import shared_task

from decimal import Decimal

from currency import model_choices as mch
from currency.data_source.service import previous_record_check_and_save, log


# 980 UAH
# 978 EUR
# 840 USD
@shared_task()
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
