"""Contract tests for /api/v1/accounts."""

from rest_framework import status
from rest_framework.test import APIClient

from seven23.tests.contracts.v1.base import ApiContractTestCase
from seven23.tests.contracts.v1.schemas import ACCOUNT_V1, DRF_DETAIL_V1, DRF_VALIDATION_V1
from seven23.tests.contracts.shapes import AnyOf, ListOf, assert_json_shape


class AccountsContractTest(ApiContractTestCase):
    def test_list_shape(self):
        response = self.client.get('/api/v1/accounts')
        data = self.assertJsonResponse(response, ListOf(ACCOUNT_V1, allow_empty=False))
        self.assertEqual(data[0]['id'], self.account.id)
        self.assertEqual(data[0]['name'], self.account.name)
        self.assertEqual(data[0]['currency'], self.usd.id)

    def test_list_unauthenticated_shape(self):
        client = APIClient()
        response = client.get('/api/v1/accounts')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        assert_json_shape(response.json(), DRF_DETAIL_V1)

    def test_retrieve_shape(self):
        response = self.client.get(f'/api/v1/accounts/{self.account.id}')
        data = self.assertJsonResponse(response, ACCOUNT_V1)
        self.assertEqual(data['id'], self.account.id)

    def test_retrieve_other_users_account_404(self):
        response = self.client.get(f'/api/v1/accounts/{self.other_account.id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert_json_shape(response.json(), DRF_DETAIL_V1)

    def test_create_shape(self):
        response = self.client.post(
            '/api/v1/accounts',
            {'name': 'New Contract Account', 'currency': self.eur.id},
            format='json',
        )
        data = self.assertJsonResponse(
            response, ACCOUNT_V1, expected_status=status.HTTP_201_CREATED
        )
        self.assertEqual(data['name'], 'New Contract Account')
        self.assertEqual(data['currency'], self.eur.id)
        self.assertFalse(data['archived'])
        self.assertFalse(data['public'])

    def test_create_validation_error_shape(self):
        response = self.client.post('/api/v1/accounts', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_update_put_shape(self):
        response = self.client.put(
            f'/api/v1/accounts/{self.account.id}',
            {
                'name': 'Renamed',
                'currency': self.usd.id,
                'archived': False,
                'public': True,
                'preferences': '{"theme":"dark"}',
            },
            format='json',
        )
        data = self.assertJsonResponse(response, ACCOUNT_V1)
        self.assertEqual(data['name'], 'Renamed')
        self.assertTrue(data['public'])

    def test_update_patch_shape(self):
        response = self.client.patch(
            f'/api/v1/accounts/{self.account.id}',
            {'name': 'Patched Name'},
            format='json',
        )
        data = self.assertJsonResponse(response, ACCOUNT_V1)
        self.assertEqual(data['name'], 'Patched Name')

    def test_destroy_shape(self):
        response = self.client.delete(f'/api/v1/accounts/{self.account.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_bulk_create_shape(self):
        response = self.client.post(
            '/api/v1/accounts',
            [
                {'name': 'Bulk A', 'currency': self.usd.id},
                {'name': 'Bulk B', 'currency': self.eur.id},
            ],
            format='json',
        )
        data = self.assertJsonResponse(
            response, ListOf(ACCOUNT_V1, allow_empty=False), expected_status=status.HTTP_201_CREATED
        )
        self.assertEqual(len(data), 2)

    def test_bulk_update_shape(self):
        response = self.client.put(
            '/api/v1/accounts',
            [
                {
                    'id': self.account.id,
                    'name': 'Bulk Updated',
                    'currency': self.usd.id,
                }
            ],
            format='json',
        )
        data = self.assertJsonResponse(response, ListOf(ACCOUNT_V1, allow_empty=False))
        self.assertEqual(data[0]['name'], 'Bulk Updated')

    def test_bulk_partial_update_shape(self):
        response = self.client.patch(
            '/api/v1/accounts',
            [{'id': self.account.id, 'name': 'Bulk Patched'}],
            format='json',
        )
        data = self.assertJsonResponse(response, ListOf(ACCOUNT_V1, allow_empty=False))
        self.assertEqual(data[0]['name'], 'Bulk Patched')

    def test_bulk_destroy_with_ids_shape(self):
        response = self.client.delete(
            '/api/v1/accounts',
            [self.account.id],
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_bulk_destroy_without_ids_rejected(self):
        response = self.client.delete('/api/v1/accounts', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
