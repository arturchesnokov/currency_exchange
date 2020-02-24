import requests
from decimal import Decimal
from celery import shared_task

from currency import model_choices as mch
from currency.data_source.service import previous_record_check_and_save, log


@shared_task()
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
