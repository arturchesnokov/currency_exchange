import pytest
from django.urls import reverse
from currency.models import Rate
from currency.data_source.bank_privatbank import _privat
from currency.data_source.bank_monobank import _mono

from account.tasks import send_email_async
from uuid import uuid4
from decimal import Decimal

from tests.helpers import DbHelpers as helper


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


def test_rates_auth(api_client, user):
    url = reverse('api-currency:rates')
    response = api_client.get(url)
    assert response.status_code == 401

    api_client.login(user.username, user.raw_password)
    response = api_client.get(url)

    assert response.status_code == 200


def test_get_rates(api_client, user):  # GET
    print('test_get_rates started')
    api_client.login(user.username, user.raw_password)

    helper.create_rate('1', 10.5, 15.93, '1')
    helper.create_rate('1', 11.12, 18.4, '1')
    helper.create_rate('2', 12.55, 19.5, '1')

    url = reverse('api-currency:rates')
    response = api_client.get(url)
    print('Response->json: ', response.json())
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_create_rate(api_client, user):  # POST
    print("test_create_rate started")
    api_client.login(user.username, user.raw_password)

    url = reverse('api-currency:rates')
    data = {"currency": "1",
            "buy": 10.55,
            "sale": 20,
            "source": "1"}

    response = api_client.post(url, data)
    print('Response->json: ', response.json())
    assert response.status_code == 201
    r_id = response.json()['id']
    assert helper.get_rate(r_id)


def test_get_rate(api_client, user):  # GET by id
    print('test_get_rate started')
    api_client.login(user.username, user.raw_password)

    r_id = helper.create_rate('1', 11.11, 22.22, '1')

    response = api_client.get(reverse('api-currency:rate', args=(r_id,)))
    print('Response->json: ', response.json())
    assert response.status_code == 200
    assert response.json()['id'] == r_id


def test_delete_rate(api_client, user):  # Delete by id
    print('test_delete_rate started')
    api_client.login(user.username, user.raw_password)

    r_id = helper.create_rate('1', 12.12, 23.23, '1')

    assert helper.get_rate(r_id)

    response = api_client.delete(reverse('api-currency:rate', args=(r_id,)))
    assert response.status_code == 204
    assert helper.get_rate(r_id) is None


def test_put_rate(api_client, user):  # PUT by id
    print('test_put_rate started')
    api_client.login(user.username, user.raw_password)

    r_id = helper.create_rate('1', 12.34, 45.67, '1')

    url = reverse('api-currency:rate', args=(r_id,))
    data = {"currency": "2",  # new value
            "buy": 12.34,
            "sale": 45.99,  # new value
            "source": "1"}
    response = api_client.put(url, data)

    print('Response->json: ', response.json())
    assert response.status_code == 200
    assert response.json()['sale'] == '45.99'
    assert helper.get_rate(r_id).currency == 2


def test_patch_rate(api_client, user):  # PATCH by id
    print('test_patch_rate started')
    api_client.login(user.username, user.raw_password)

    r_id = helper.create_rate('1', 12.34, 45.67, '1')

    url = reverse('api-currency:rate', args=(r_id,))
    data = {"currency": "2", }  # new value

    response = api_client.patch(url, data)

    print('Response->json: ', response.json())
    assert response.status_code == 200
    assert helper.get_rate(r_id).currency == 2


# Contacts

def test_get_contacts(api_client, user):  # GET
    print('test_get_contacts started')
    api_client.login(user.username, user.raw_password)

    helper.create_contact(user.email, 'title 1', 'Text 1')
    helper.create_contact(user.email, 'title 2', 'Text 2')
    helper.create_contact(user.email, 'title 3', 'Text 3')

    url = reverse('api-account:contacts')
    response = api_client.get(url)
    print('Response->json: ', response.json())
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_create_contact(api_client, user):  # POST
    print("test_create_contact started")
    api_client.login(user.username, user.raw_password)

    url = reverse('api-account:contacts')

    data = {"email": user.email,
            "title": 'title 1',
            "text": 'Text 1'}

    response = api_client.post(url, data)
    print('Response->json: ', response.json())
    assert response.status_code == 201
    c_id = response.json()['id']
    assert helper.get_contact(c_id)


def test_get_contact(api_client, user):  # GET by id
    print('test_get_contact by id started')
    api_client.login(user.username, user.raw_password)

    c_id = helper.create_contact(user.email, 'title 1', 'Text 1')

    response = api_client.get(reverse('api-account:contact', args=(c_id,)))
    print('Response->json: ', response.json())
    assert response.status_code == 200
    assert response.json()['id'] == c_id


def test_delete_contact(api_client, user):  # Delete by id
    print('test_delete_contact by id started')
    api_client.login(user.username, user.raw_password)

    c_id = helper.create_contact(user.email, 'title 1', 'Text 1')

    assert helper.get_contact(c_id)

    response = api_client.delete(reverse('api-account:contact', args=(c_id,)))
    assert response.status_code == 405
    assert helper.get_contact(c_id)


def test_put_contact(api_client, user):  # PUT by id
    print('test_put_contact by id started')
    api_client.login(user.username, user.raw_password)

    c_id = helper.create_contact(user.email, 'title 1', 'Text 1')

    url = reverse('api-account:contact', args=(c_id,))
    data = {"email": user.email,
            "title": 'title 2',  # new value
            "text": 'Text 2'}  # new value

    response = api_client.put(url, data)

    print('Response->json: ', response.json())
    assert response.status_code == 200
    assert response.json()['title'] == 'title 2'
    assert response.json()['text'] == 'Text 2'


def test_patch_contact(api_client, user):  # PATCH by id
    print('test_patch_contact by id started')
    api_client.login(user.username, user.raw_password)

    c_id = helper.create_contact(user.email, 'title 1', 'Text 1')

    url = reverse('api-account:contact', args=(c_id,))
    data = {"title": 'title 2'}  # new value

    response = api_client.patch(url, data)

    print('Response->json: ', response.json())
    assert response.status_code == 200
    assert response.json()['title'] == 'title 2'


class Response:
    pass


# def test_task_bank_privatbank(mocker):
#     def mock():
#         response = Response()
#         response.json = lambda: [
#             {"ccy": "USD", "base_ccy": "UAH", "buy": "27.77", "sale": "28.88"},
#             {"ccy": "EUR", "base_ccy": "UAH", "buy": "28.88", "sale": "29.99"},
#             {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.22", "sale": "0.33"}
#         ]
#         return response
#
#     requests_get_patcher = mocker.patch('requests.get')
#     requests_get_patcher.return_value = mock()
#
#     Rate.objects.all().delete()
#
#     _privat()
#     rate = Rate.objects.all()
#     assert len(rate) == 2  # because only 2 currencies parsed
#     usd = rate[0]
#     assert usd.currency == 1
#     assert usd.buy == Decimal('27.77')
#     assert usd.sale == Decimal('28.88')
#     assert rate[0].source == 1
#
#     eur = rate[1]
#     assert eur.currency == 2
#     assert eur.buy == Decimal('28.88')
#     assert eur.sale == Decimal('29.99')
#     assert eur.source == 1
#     Rate.objects.all().delete()


def test_task_nomo(mocker):
    def mock():
        response = Response()
        response.json = lambda: [
            {"currencyCodeA": 840, "currencyCodeB": 980, "rateBuy": 27.77, "rateSell": 28.88},
            {"currencyCodeA": 978, "currencyCodeB": 980, "rateBuy": 28.88, "rateSell": 29.99},
            {"currencyCodeA": 643, "currencyCodeB": 980, "rateBuy": 0.22, "rateSell": 0.33}
        ]
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    _mono()
    rate = Rate.objects.all()
    assert len(rate) == 2  # because only 2 currencies parsed
    usd = rate[0]
    assert usd.currency == 1
    assert usd.buy == Decimal('27.77')
    assert usd.sale == Decimal('28.88')
    assert rate[0].source == 1

    eur = rate[1]
    assert eur.currency == 2
    assert eur.buy == Decimal('28.88')
    assert eur.sale == Decimal('29.99')
    assert eur.source == 1
    Rate.objects.all().delete()
