from rest_framework.test import APITestCase

from account.models import User
from currency_exchange import settings
from django.test import TestCase
from django.urls import reverse


class ApiRateTestCase(APITestCase):
    # @classmethod
    # def setUpClass(cls):
    #     user = User.objects.create_user('username', 'Pas$w0rd')
    #     cls.client.force_authenticate(user)

    def create_rate(self, currency, buy_rate, sale_rate, source):
        user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(user)
        url = reverse('api-currency:rates')
        data = {"currency": currency,
                "buy": buy_rate,
                "sale": sale_rate,
                "source": source}
        self.client.post(url, data)

    def test_create_rate(self):
        user = User.objects.create_user('username', 'Pas$w0rd')
        self.client.force_authenticate(user)
        url = reverse('api-currency:rates')
        data = {"currency": "1",
                "buy": 10,
                "sale": 10,
                "source": "1"}
        response = self.client.post(url, data)
        print('Resp', response)
        print('Content', response.content)
        self.assertEqual(response.status_code, 201)

    def test_get_rates(self):
        ApiRateTestCase.create_rate(self, '1', 10.5, 15.9, '1')
        # user = User.objects.create_user('username', 'Pas$w0rd')
        # self.client.force_authenticate(user)
        response = self.client.get(reverse('api-currency:rates'))
        print(reverse('api-currency:rates'))
        print('Resp', response)
        print('Content', response.content)
        self.assertEqual(response.status_code, 200)

    def test_always_pass(self):
        assert True
