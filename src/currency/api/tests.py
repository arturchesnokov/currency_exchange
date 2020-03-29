from rest_framework.test import APITestCase
from decimal import Decimal

from account.models import User
from currency.models import Rate
from django.urls import reverse


# python manage.py test -v 2
class ApiRateTestCase(APITestCase):

    @staticmethod
    def create_rate(currency, buy_rate, sale_rate, source):
        r = Rate(currency=currency, buy=buy_rate, sale=sale_rate, source=source)
        r.save()
        return r.id

    @staticmethod
    def get_rate(rate_id):
        try:
            return Rate.objects.get(id=rate_id)
        except Rate.DoesNotExist:
            return None

    def test_get_rates(self):  # GET
        print('test_get_rates started')
        user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(user)

        ApiRateTestCase.create_rate('1', 10.5, 15.93, '1')
        ApiRateTestCase.create_rate('1', 11.12, 18.4, '1')
        ApiRateTestCase.create_rate('2', 12.55, 19.5, '1')

        response = self.client.get(reverse('api-currency:rates'))
        print('Response->json: ', response.json())
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_create_rate(self):  # POST
        print("test_create_rate started")
        user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(user)
        url = reverse('api-currency:rates')
        data = {"currency": "1",
                "buy": 10.55,
                "sale": 20,
                "source": "1"}
        response = self.client.post(url, data)
        print('Response->json: ', response.json())
        assert response.status_code == 201
        r_id = response.json()['id']
        assert ApiRateTestCase.get_rate(r_id)

    def test_get_rate(self):  # GET by id
        print('test_get_rate started')
        user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(user)

        r_id = ApiRateTestCase.create_rate('1', 11.11, 22.22, '1')

        response = self.client.get(reverse('api-currency:rate', args=(r_id,)))
        print('Response->json: ', response.json())
        assert response.status_code == 200
        assert response.json()['id'] == r_id

    def test_delete_rate(self):  # Delete by id
        print('test_delete_rate started')
        user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(user)

        r_id = ApiRateTestCase.create_rate('1', 12.12, 23.23, '1')

        assert ApiRateTestCase.get_rate(r_id)

        response = self.client.delete(reverse('api-currency:rate', args=(r_id,)))
        assert response.status_code == 204
        assert ApiRateTestCase.get_rate(r_id) is None

    def test_put_rate(self):  # PUT by id
        print('test_put_rate started')
        user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(user)

        r_id = ApiRateTestCase.create_rate('1', 12.34, 45.67, '1')

        url = reverse('api-currency:rate', args=(r_id,))
        data = {"currency": "2",  # new value
                "buy": 12.34,
                "sale": 45.99,  # new value
                "source": "1"}
        response = self.client.put(url, data)

        print('Response->json: ', response.json())
        assert response.status_code == 200
        assert response.json()['sale'] == '45.99'
        assert ApiRateTestCase.get_rate(r_id).currency == 2

    def test_patch_rate(self):  # PATCH by id
        print('test_patch_rate started')
        user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(user)

        r_id = ApiRateTestCase.create_rate('1', 12.34, 45.67, '1')

        url = reverse('api-currency:rate', args=(r_id,))
        data = {"currency": "2",}  # new value

        response = self.client.patch(url, data)

        print('Response->json: ', response.json())
        assert response.status_code == 200
        assert ApiRateTestCase.get_rate(r_id).currency == 2