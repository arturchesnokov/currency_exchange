import pytest
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from account.models import User
from currency.data_source import bank_privatbank

from account.tasks import send_email_async


def test_sanity():
    assert 200 == 200


def test_index_page(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


def test_get_rates_not_auth(client):
    url = reverse('api-currency:rates')
    response = client.get(url)
    assert response.status_code == 401
    resp_j = response.json()
    assert len(resp_j) == 1
    assert resp_j['detail'] == 'Authentication credentials were not provided.'


# @pytest.mark.django_db
# def test_get_rates_auth(api_client):
#     url = reverse('api-currency:rates')
#     response = api_client.get(url)
#     assert response.status_code == 401
#
#     # create user
#     email = 'srjgkbdrgjdbr@mail.com'
#     password = '1234567'
#     user = User.objects.create(email=email, username=email)
#     user.set_password(password)
#     user.save()
#
#     api_client.login(email, password)
#
#     response = api_client.get(url)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_get_rates(api_client):
#     url = reverse('api-currency:rates')
#
#
#     api_client = APIClient()

class Response:
    pass

@pytest.mark.django_db
def test_task(mocker):

    def mock():
        response = Response()
        response.json = lambda: [{"ccy":"USD","base_ccy":"UAH","buy":"27.35000","sale":"27.80000"},{"ccy":"EUR","base_ccy":"UAH","buy":"29.65000","sale":"30.40000"},{"ccy":"RUR","base_ccy":"UAH","buy":"0.32000","sale":"0.36000"},{"ccy":"BTC","base_ccy":"USD","buy":"6629.4800","sale":"7327.3200"}]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    bank_privatbank()

@pytest.mark.django_db
def test_send_email(mocker):
    from django.core import mail
    from uuid import uuid4

    emails = mail.outbox
    print('EMAILS:', emails)

    send_email_async(1, str(uuid4()))
    emails = mail.outbox
    print('EMAILS', emails)