from datetime import timedelta, date, datetime
import requests

from django.core.management.base import BaseCommand
from currency.models import Rate

from decimal import Decimal
from currency import model_choices as mch
from currency.data_source.service import log


class Command(BaseCommand):
    help = 'Get PrivatBank archive currency rates'

    def handle(self, *args, **options):
        request_date = date(2019, 1, 1)
        final_date = date(2020, 1, 1)

        while request_date < final_date:
            privat_on_date(request_date)
            # if Rate.objects.filter(source=mch.SR_PRIVAT, created=request_date).last():
            #     privat_on_date(request_date)
            # else:
            #     print(f'record for {request_date} already exists')

            request_date += timedelta(days=1)


def privat_on_date(r_date):
    log.info(f'PrivatBank on {r_date} parser started')
    request_date = datetime.strftime(r_date, "%d.%m.%Y")

    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={request_date}'  # TODO change hardcode data
    rates = requests.get(url).json()['exchangeRate']

    for rate in rates:
        if rate.get('currency') is not None:
            if rate['currency'] in {'USD', 'EUR'}:
                currency = mch.CURR_USD if rate['currency'] == 'USD' else mch.CURR_EUR

                rate_kwargs = {
                    'currency': currency,
                    'buy': Decimal(rate['purchaseRate']),
                    'sale': Decimal(rate['saleRate']),
                    'source': mch.SR_PRIVAT,
                    'created': r_date,
                }
                previous_record_check_and_save(rate_kwargs)  # TODO check exist or not by date and currency
                print('rate_kwargs:', rate_kwargs)


# check previous record with currency and source, if currency rate changed - save it
def previous_record_check_and_save(rate_kwargs):
    new_rate = Rate(**rate_kwargs)  # create new instance of currency record

    # get last currency record for date
    last_rate = Rate.objects.filter(currency=new_rate.currency, source=new_rate.source, created=new_rate.created).last()

    # verify and save if no record for this date
    if last_rate is None:
        new_rate.save()
        new_rate.created = rate_kwargs['created']
        new_rate.save(update_fields=['created', ])
