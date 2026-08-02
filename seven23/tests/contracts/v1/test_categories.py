"""Contract tests for /api/v1/categories."""

from rest_framework import status
from rest_framework.test import APIClient

from seven23.tests.contracts.v1.base import ApiContractTestCase
from seven23.tests.contracts.v1.schemas import (
    BLOB_RESOURCE_V1,
    DRF_DETAIL_V1,
    DRF_VALIDATION_V1,
)
from seven23.tests.contracts.shapes import AnyOf, ListOf, assert_json_shape
from seven23.models.categories.models import Category


class CategoriesContractTest(ApiContractTestCase):
    def test_list_shape(self):
        response = self.client.get('/api/v1/categories')
        data = self.assertJsonResponse(response, ListOf(BLOB_RESOURCE_V1, allow_empty=False))
        self.assertEqual(data[0]['account'], self.account.id)

    def test_list_filter_by_account_shape(self):
        response = self.client.get(f'/api/v1/categories?account={self.account.id}')
        data = self.assertJsonResponse(response, ListOf(BLOB_RESOURCE_V1))
        for item in data:
            self.assertEqual(item['account'], self.account.id)

    def test_list_filter_last_edited_includes_deleted_shape(self):
        self.category.deleted = True
        self.category.save()
        response = self.client.get(
            f'/api/v1/categories?last_edited=2000-01-01T00:00:00Z'
        )
        data = self.assertJsonResponse(response, ListOf(BLOB_RESOURCE_V1))
        self.assertTrue(any(item['deleted'] for item in data))

    def test_list_unauthenticated_shape(self):
        client = APIClient()
        response = client.get('/api/v1/categories')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        assert_json_shape(response.json(), DRF_DETAIL_V1)

    def test_retrieve_shape(self):
        response = self.client.get(f'/api/v1/categories/{self.category.id}')
        data = self.assertJsonResponse(response, BLOB_RESOURCE_V1)
        self.assertEqual(data['id'], self.category.id)
        self.assertEqual(data['blob'], self.category.blob)

    def test_create_shape(self):
        response = self.client.post(
            '/api/v1/categories',
            {'account': self.account.id, 'blob': '{"name":"Transport"}'},
            format='json',
        )
        data = self.assertJsonResponse(
            response, BLOB_RESOURCE_V1, expected_status=status.HTTP_201_CREATED
        )
        self.assertEqual(data['blob'], '{"name":"Transport"}')
        self.assertFalse(data['deleted'])
        self.assertTrue(data['active'])

    def test_create_validation_error_shape(self):
        response = self.client.post(
            '/api/v1/categories',
            {'account': 999999, 'blob': '{"name":"X"}'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_update_put_shape(self):
        response = self.client.put(
            f'/api/v1/categories/{self.category.id}',
            {
                'account': self.account.id,
                'blob': '{"name":"Updated"}',
                'active': True,
                'deleted': False,
            },
            format='json',
        )
        data = self.assertJsonResponse(response, BLOB_RESOURCE_V1)
        self.assertEqual(data['blob'], '{"name":"Updated"}')

    def test_update_patch_shape(self):
        response = self.client.patch(
            f'/api/v1/categories/{self.category.id}',
            {'blob': '{"name":"Patched"}'},
            format='json',
        )
        data = self.assertJsonResponse(response, BLOB_RESOURCE_V1)
        self.assertEqual(data['blob'], '{"name":"Patched"}')

    def test_destroy_returns_serialized_body_shape(self):
        # Categories destroy intentionally returns the serialized instance
        response = self.client.delete(f'/api/v1/categories/{self.category.id}')
        data = self.assertJsonResponse(response, BLOB_RESOURCE_V1)
        self.assertEqual(data['id'], self.category.id)

    def test_bulk_create_shape(self):
        response = self.client.post(
            '/api/v1/categories',
            [
                {'account': self.account.id, 'blob': '{"name":"A"}'},
                {'account': self.account.id, 'blob': '{"name":"B"}'},
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
            '/api/v1/categories',
            [
                {
                    'id': self.category.id,
                    'account': self.account.id,
                    'blob': '{"name":"Bulk"}',
                }
            ],
            format='json',
        )
        data = self.assertJsonResponse(response, ListOf(BLOB_RESOURCE_V1, allow_empty=False))
        self.assertEqual(data[0]['blob'], '{"name":"Bulk"}')

    def test_bulk_partial_update_shape(self):
        response = self.client.patch(
            '/api/v1/categories',
            [{'id': self.category.id, 'blob': '{"name":"BulkPatch"}'}],
            format='json',
        )
        data = self.assertJsonResponse(response, ListOf(BLOB_RESOURCE_V1, allow_empty=False))
        self.assertEqual(data[0]['blob'], '{"name":"BulkPatch"}')

    def test_bulk_destroy_shape(self):
        extra = Category.objects.create(account=self.account, blob='{"name":"tmp"}')
        response = self.client.delete('/api/v1/categories', [extra.id], format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_bulk_destroy_without_ids_rejected(self):
        response = self.client.delete('/api/v1/categories', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
