import requests
from decimal import Decimal

from currency import model_choices as mch
from currency.data_source.service import previous_record_check_and_save, log

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