"""Contract tests for /api/v1/debitscredits."""

from rest_framework import status
from rest_framework.test import APIClient

from seven23.tests.contracts.v1.base import ApiContractTestCase
from seven23.tests.contracts.v1.schemas import (
    DEBITSCREDITS_V1,
    DRF_DETAIL_V1,
    DRF_VALIDATION_V1,
)
from seven23.tests.contracts.shapes import AnyOf, ListOf, assert_json_shape
from seven23.models.transactions.models import DebitsCredits


class DebitsCreditsContractTest(ApiContractTestCase):
    def test_list_shape(self):
        response = self.client.get('/api/v1/debitscredits')
        data = self.assertJsonResponse(
            response, ListOf(DEBITSCREDITS_V1, allow_empty=False)
        )
        self.assertGreaterEqual(len(data), 2)

    def test_list_omits_null_category_key(self):
        response = self.client.get('/api/v1/debitscredits')
        data = response.json()
        without_category = [item for item in data if item['id'] == self.debit_no_category.id]
        self.assertEqual(len(without_category), 1)
        self.assertNotIn('category', without_category[0])
        self.assertShape(without_category[0], DEBITSCREDITS_V1)

    def test_list_includes_category_when_set(self):
        response = self.client.get('/api/v1/debitscredits')
        data = response.json()
        with_category = [item for item in data if item['id'] == self.debit.id]
        self.assertEqual(len(with_category), 1)
        self.assertIn('category', with_category[0])
        self.assertEqual(with_category[0]['category'], self.category.id)
        self.assertShape(with_category[0], DEBITSCREDITS_V1)

    def test_list_filter_by_account_shape(self):
        response = self.client.get(f'/api/v1/debitscredits?account={self.account.id}')
        data = self.assertJsonResponse(response, ListOf(DEBITSCREDITS_V1))
        for item in data:
            self.assertEqual(item['account'], self.account.id)

    def test_list_filter_last_edited_shape(self):
        response = self.client.get(
            '/api/v1/debitscredits?last_edited=2000-01-01T00:00:00Z'
        )
        self.assertJsonResponse(response, ListOf(DEBITSCREDITS_V1))

    def test_list_unauthenticated_shape(self):
        client = APIClient()
        response = client.get('/api/v1/debitscredits')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        assert_json_shape(response.json(), DRF_DETAIL_V1)

    def test_retrieve_shape(self):
        response = self.client.get(f'/api/v1/debitscredits/{self.debit.id}')
        data = self.assertJsonResponse(response, DEBITSCREDITS_V1)
        self.assertEqual(data['id'], self.debit.id)
        self.assertEqual(data['category'], self.category.id)

    def test_create_with_category_shape(self):
        response = self.client.post(
            '/api/v1/debitscredits',
            {
                'account': self.account.id,
                'category': self.category.id,
                'blob': '{"amount":-9}',
            },
            format='json',
        )
        data = self.assertJsonResponse(
            response, DEBITSCREDITS_V1, expected_status=status.HTTP_201_CREATED
        )
        self.assertEqual(data['category'], self.category.id)

    def test_create_without_category_shape(self):
        response = self.client.post(
            '/api/v1/debitscredits',
            {'account': self.account.id, 'blob': '{"amount":-1}'},
            format='json',
        )
        data = self.assertJsonResponse(
            response, DEBITSCREDITS_V1, expected_status=status.HTTP_201_CREATED
        )
        self.assertNotIn('category', data)

    def test_create_validation_error_shape(self):
        response = self.client.post('/api/v1/debitscredits', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_update_put_shape(self):
        response = self.client.put(
            f'/api/v1/debitscredits/{self.debit.id}',
            {
                'account': self.account.id,
                'category': self.category.id,
                'blob': '{"amount":-99}',
                'active': True,
                'deleted': False,
            },
            format='json',
        )
        data = self.assertJsonResponse(response, DEBITSCREDITS_V1)
        self.assertEqual(data['blob'], '{"amount":-99}')

    def test_update_patch_shape(self):
        response = self.client.patch(
            f'/api/v1/debitscredits/{self.debit.id}',
            {'blob': '{"amount":-3}'},
            format='json',
        )
        data = self.assertJsonResponse(response, DEBITSCREDITS_V1)
        self.assertEqual(data['blob'], '{"amount":-3}')

    def test_destroy_shape(self):
        response = self.client.delete(f'/api/v1/debitscredits/{self.debit.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_bulk_create_shape(self):
        response = self.client.post(
            '/api/v1/debitscredits',
            [
                {'account': self.account.id, 'blob': '{"n":1}'},
                {
                    'account': self.account.id,
                    'category': self.category.id,
                    'blob': '{"n":2}',
                },
            ],
            format='json',
        )
        data = self.assertJsonResponse(
            response,
            ListOf(DEBITSCREDITS_V1, allow_empty=False),
            expected_status=status.HTTP_201_CREATED,
        )
        self.assertEqual(len(data), 2)

    def test_bulk_update_shape(self):
        response = self.client.put(
            '/api/v1/debitscredits',
            [
                {
                    'id': self.debit.id,
                    'account': self.account.id,
                    'blob': '{"bulk":true}',
                }
            ],
            format='json',
        )
        data = self.assertJsonResponse(
            response, ListOf(DEBITSCREDITS_V1, allow_empty=False)
        )
        self.assertEqual(data[0]['blob'], '{"bulk":true}')

    def test_bulk_partial_update_shape(self):
        response = self.client.patch(
            '/api/v1/debitscredits',
            [{'id': self.debit.id, 'blob': '{"patched":true}'}],
            format='json',
        )
        data = self.assertJsonResponse(
            response, ListOf(DEBITSCREDITS_V1, allow_empty=False)
        )
        self.assertEqual(data[0]['blob'], '{"patched":true}')

    def test_bulk_destroy_shape(self):
        extra = DebitsCredits.objects.create(
            account=self.account, blob='{"tmp":true}'
        )
        response = self.client.delete(
            '/api/v1/debitscredits', [extra.id], format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_bulk_destroy_without_ids_rejected(self):
        response = self.client.delete('/api/v1/debitscredits', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
