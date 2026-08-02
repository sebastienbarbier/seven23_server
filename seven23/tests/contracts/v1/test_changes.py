"""Contract tests for /api/v1/changes."""

from rest_framework import status
from rest_framework.test import APIClient

from seven23.tests.contracts.v1.base import ApiContractTestCase
from seven23.tests.contracts.v1.schemas import (
    BLOB_RESOURCE_V1,
    DRF_DETAIL_V1,
    DRF_VALIDATION_V1,
)
from seven23.tests.contracts.shapes import AnyOf, ListOf, assert_json_shape
from seven23.models.transactions.models import Change


class ChangesContractTest(ApiContractTestCase):
    def test_list_shape(self):
        response = self.client.get('/api/v1/changes')
        data = self.assertJsonResponse(response, ListOf(BLOB_RESOURCE_V1, allow_empty=False))
        self.assertEqual(data[0]['id'], self.change.id)

    def test_list_filter_by_account_shape(self):
        response = self.client.get(f'/api/v1/changes?account={self.account.id}')
        data = self.assertJsonResponse(response, ListOf(BLOB_RESOURCE_V1))
        for item in data:
            self.assertEqual(item['account'], self.account.id)

    def test_list_filter_last_edited_shape(self):
        response = self.client.get('/api/v1/changes?last_edited=2000-01-01T00:00:00Z')
        self.assertJsonResponse(response, ListOf(BLOB_RESOURCE_V1))

    def test_list_unauthenticated_shape(self):
        client = APIClient()
        response = client.get('/api/v1/changes')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        assert_json_shape(response.json(), DRF_DETAIL_V1)

    def test_retrieve_shape(self):
        response = self.client.get(f'/api/v1/changes/{self.change.id}')
        data = self.assertJsonResponse(response, BLOB_RESOURCE_V1)
        self.assertEqual(data['blob'], self.change.blob)

    def test_create_shape(self):
        response = self.client.post(
            '/api/v1/changes',
            {'account': self.account.id, 'blob': '{"rate":1.1}'},
            format='json',
        )
        data = self.assertJsonResponse(
            response, BLOB_RESOURCE_V1, expected_status=status.HTTP_201_CREATED
        )
        self.assertEqual(data['blob'], '{"rate":1.1}')

    def test_create_validation_error_shape(self):
        response = self.client.post('/api/v1/changes', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_update_put_shape(self):
        response = self.client.put(
            f'/api/v1/changes/{self.change.id}',
            {
                'account': self.account.id,
                'blob': '{"rate":2.0}',
                'active': True,
                'deleted': False,
            },
            format='json',
        )
        data = self.assertJsonResponse(response, BLOB_RESOURCE_V1)
        self.assertEqual(data['blob'], '{"rate":2.0}')

    def test_update_patch_shape(self):
        response = self.client.patch(
            f'/api/v1/changes/{self.change.id}',
            {'blob': '{"rate":3.0}'},
            format='json',
        )
        data = self.assertJsonResponse(response, BLOB_RESOURCE_V1)
        self.assertEqual(data['blob'], '{"rate":3.0}')

    def test_destroy_shape(self):
        response = self.client.delete(f'/api/v1/changes/{self.change.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_bulk_create_shape(self):
        response = self.client.post(
            '/api/v1/changes',
            [
                {'account': self.account.id, 'blob': '{"n":1}'},
                {'account': self.account.id, 'blob': '{"n":2}'},
            ],
            format='json',
        )
        data = self.assertJsonResponse(
            response,
            ListOf(BLOB_RESOURCE_V1, allow_empty=False),
            expected_status=status.HTTP_201_CREATED,
        )
        self.assertEqual(len(data), 2)

    def test_bulk_update_shape(self):
        response = self.client.put(
            '/api/v1/changes',
            [
                {
                    'id': self.change.id,
                    'account': self.account.id,
                    'blob': '{"bulk":true}',
                }
            ],
            format='json',
        )
        data = self.assertJsonResponse(response, ListOf(BLOB_RESOURCE_V1, allow_empty=False))
        self.assertEqual(data[0]['blob'], '{"bulk":true}')

    def test_bulk_partial_update_shape(self):
        response = self.client.patch(
            '/api/v1/changes',
            [{'id': self.change.id, 'blob': '{"patched":true}'}],
            format='json',
        )
        data = self.assertJsonResponse(response, ListOf(BLOB_RESOURCE_V1, allow_empty=False))
        self.assertEqual(data[0]['blob'], '{"patched":true}')

    def test_bulk_destroy_shape(self):
        extra = Change.objects.create(account=self.account, blob='{"tmp":true}')
        response = self.client.delete('/api/v1/changes', [extra.id], format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_bulk_destroy_without_ids_rejected(self):
        response = self.client.delete('/api/v1/changes', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
