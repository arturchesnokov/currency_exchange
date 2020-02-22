from celery import shared_task

from currency.data_source.bank_privatbank import _privat
from currency.data_source.bank_monobank import _mono
from currency.data_source.bank_otp import _otp
from currency.data_source.site_vkurse_dp_ua import _vkurse_dp_ua
from currency.data_source.site_obmen_dp_ua import _obmen_dp_ua
from currency.data_source.site_finance_i_ua import _finance_i_ua


@shared_task()
def parse_rates():
    _privat()
    _mono()
    _otp()
    _vkurse_dp_ua()
    _obmen_dp_ua()
    _finance_i_ua()
