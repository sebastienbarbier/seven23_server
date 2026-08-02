"""Contract tests for /api/v1/currencies."""

from rest_framework import status
from rest_framework.test import APIClient

from seven23.tests.contracts.v1.base import ApiContractTestCase
from seven23.tests.contracts.v1.schemas import CURRENCY_V1, DRF_DETAIL_V1
from seven23.tests.contracts.shapes import ListOf, assert_json_shape


class CurrenciesContractTest(ApiContractTestCase):
    def test_list_shape(self):
        # Currencies are AllowAny — also test anonymous access
        client = APIClient()
        response = client.get('/api/v1/currencies')
        data = self.assertJsonResponse(response, ListOf(CURRENCY_V1, allow_empty=False))
        codes = {item['code'] for item in data}
        self.assertIn('USD', codes)
        self.assertIn('EUR', codes)

    def test_list_authenticated_shape(self):
        response = self.client.get('/api/v1/currencies')
        self.assertJsonResponse(response, ListOf(CURRENCY_V1, allow_empty=False))

    def test_retrieve_shape(self):
        response = self.client.get(f'/api/v1/currencies/{self.usd.id}')
        data = self.assertJsonResponse(response, CURRENCY_V1)
        self.assertEqual(data['id'], self.usd.id)
        self.assertEqual(data['code'], 'USD')
        self.assertEqual(data['sign'], 'USD')
        self.assertEqual(data['name'], 'US Dollars')

    def test_retrieve_missing_404_shape(self):
        response = self.client.get('/api/v1/currencies/999999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert_json_shape(response.json(), DRF_DETAIL_V1)

    def test_post_not_allowed(self):
        response = self.client.post(
            '/api/v1/currencies',
            {'name': 'X', 'sign': 'X', 'code': 'XXX'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_not_allowed(self):
        response = self.client.put(
            f'/api/v1/currencies/{self.usd.id}',
            {'name': 'X', 'sign': 'X', 'code': 'USD'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_not_allowed(self):
        response = self.client.patch(
            f'/api/v1/currencies/{self.usd.id}',
            {'name': 'X'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_not_allowed(self):
        response = self.client.delete(f'/api/v1/currencies/{self.usd.id}')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
