from currency.models import Rate
import logging

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
