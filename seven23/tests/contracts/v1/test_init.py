"""Contract tests for GET /api/init."""

from rest_framework import status
from rest_framework.test import APIClient

from seven23.tests.contracts.v1.base import ApiContractTestCase
from seven23.tests.contracts.v1.schemas import INIT_ANONYMOUS_V1
from seven23 import settings


class InitContractTest(ApiContractTestCase):
    def test_init_anonymous_shape(self):
        client = APIClient()
        response = client.get('/api/init')
        data = self.assertJsonResponse(response, INIT_ANONYMOUS_V1)
        self.assertApiVersionContract(data)
        self.assertEqual(data['version'], settings.VERSION)
        self.assertEqual(data['saas'], settings.SAAS)
        self.assertEqual(data['allow_account_creation'], settings.ALLOW_ACCOUNT_CREATION)

    def test_init_authenticated_shape(self):
        response = self.client.get('/api/init')
        data = self.assertJsonResponse(response, INIT_ANONYMOUS_V1)
        self.assertApiVersionContract(data)

    def test_init_content_type_is_json(self):
        response = self.client.get('/api/init')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('application/json', response['Content-Type'])

    def test_init_rejects_post(self):
        response = self.client.post('/api/init', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
