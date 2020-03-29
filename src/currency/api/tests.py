from currency_exchange import settings
from django.test import TestCase
from django.urls import reverse


class ApiRateTestCase(TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     # headers = {
    #     #     'Authorization': settings.JWT_TOKEN
    #     # }
    #     pass

    def test_get_rates(self):
        headers = {
            'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg2NjQ4MzkzLCJqdGkiOiI3ODUxYjJmOWJlYzQ0ODlmOTIxYjdiMjYyM2FhMDZiOCIsInVzZXJfaWQiOjF9.mAeDoUf8sWjB6LcQf9tDEbeGpG9DD8vnS85j7E8cwpM'
            # 'Authorization': settings.JWT_TOKEN
        }
        response = self.client.get(reverse('api-currency:rates'), headers=headers)
        # print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_always_pass(self):
        assert True


