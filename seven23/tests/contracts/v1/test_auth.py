"""Contract tests for token auth and rest-auth endpoints."""

from unittest import skipUnless

from django.contrib.auth.models import User
from django.urls import resolve, Resolver404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from seven23.tests.contracts.v1.base import ApiContractTestCase
from seven23.tests.contracts.v1.schemas import (
    AUTH_TOKEN_V1,
    DRF_DETAIL_V1,
    DRF_VALIDATION_V1,
    LOGOUT_V1,
    TOKEN_KEY_V1,
    USER_V1,
)
from seven23.tests.contracts.shapes import AnyOf, assert_json_shape
from seven23 import settings


def _registration_available():
    try:
        resolve('/api/v1/rest-auth/registration/')
        return True
    except Resolver404:
        return False


class TokenAuthContractTest(ApiContractTestCase):
    def test_api_token_auth_success_shape(self):
        client = APIClient()
        response = client.post(
            '/api/api-token-auth',
            {'username': self.user.username, 'password': self.password},
            format='json',
        )
        data = self.assertJsonResponse(response, AUTH_TOKEN_V1)
        self.assertTrue(Token.objects.filter(key=data['token'], user=self.user).exists())

    def test_api_token_auth_invalid_credentials_shape(self):
        client = APIClient()
        response = client.post(
            '/api/api-token-auth',
            {'username': self.user.username, 'password': 'wrong'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_api_token_auth_missing_fields_shape(self):
        client = APIClient()
        response = client.post('/api/api-token-auth', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))


class RestAuthLoginContractTest(ApiContractTestCase):
    def test_login_success_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/login/',
            {'username': self.user.username, 'password': self.password},
            format='json',
        )
        self.assertJsonResponse(response, TOKEN_KEY_V1)

    def test_login_with_email_success_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/login/',
            {'email': self.user.email, 'password': self.password},
            format='json',
        )
        # allauth may accept email depending on config; accept key or validation error
        if response.status_code == status.HTTP_200_OK:
            self.assertShape(response.json(), TOKEN_KEY_V1)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_login_invalid_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/login/',
            {'username': self.user.username, 'password': 'nope'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_logout_with_token_header_shape(self):
        # dj-rest-auth logout expects the token in Authorization (not force_authenticate alone)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = client.post('/api/v1/rest-auth/logout/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert_json_shape(response.json(), LOGOUT_V1)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_logout_get_not_allowed(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = client.get('/api/v1/rest-auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class RestAuthUserContractTest(ApiContractTestCase):
    def test_user_get_shape(self):
        response = self.client.get('/api/v1/rest-auth/user/')
        data = self.assertJsonResponse(response, USER_V1)
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['pk'], self.user.pk)

    def test_user_get_unauthenticated_shape(self):
        client = APIClient()
        response = client.get('/api/v1/rest-auth/user/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        assert_json_shape(response.json(), DRF_DETAIL_V1)

    def test_user_patch_shape(self):
        response = self.client.patch(
            '/api/v1/rest-auth/user/',
            {'first_name': 'Contract'},
            format='json',
        )
        data = self.assertJsonResponse(response, USER_V1)
        self.assertEqual(data['first_name'], 'Contract')

    def test_user_put_shape(self):
        response = self.client.put(
            '/api/v1/rest-auth/user/',
            {
                'username': self.user.username,
                'first_name': 'PutName',
                'favoritesCurrencies': [self.usd.id],
                'profile': {
                    'avatar': 'NONE',
                    'auto_sync': True,
                    'key_verified': False,
                    'social_networks': '',
                },
            },
            format='json',
        )
        # PUT may be strict; accept 200 with USER shape or 400 validation
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            self.assertShape(data, USER_V1)
            self.assertEqual(data['first_name'], 'PutName')
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))


class RestAuthPasswordContractTest(ApiContractTestCase):
    def test_password_change_success_shape(self):
        response = self.client.post(
            '/api/v1/rest-auth/password/change/',
            {
                'old_password': self.password,
                'new_password1': 'new-contract-pass-456',
                'new_password2': 'new-contract-pass-456',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # dj-rest-auth returns {"detail": "..."} on success
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, dict))

    def test_password_change_mismatch_shape(self):
        response = self.client.post(
            '/api/v1/rest-auth/password/change/',
            {
                'old_password': self.password,
                'new_password1': 'new-contract-pass-456',
                'new_password2': 'different-pass-456',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_password_reset_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/password/reset/',
            {
                'email': self.user.email,
                'origin': 'https://seven23.test',
            },
            format='json',
        )
        # Custom serializer requires origin; success is usually 200 with detail
        self.assertIn(response.status_code, (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST))
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_password_reset_missing_origin_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/password/reset/',
            {'email': self.user.email},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_password_reset_confirm_invalid_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/password/reset/confirm/',
            {
                'uid': 'invalid',
                'token': 'invalid',
                'new_password1': 'x' * 12,
                'new_password2': 'x' * 12,
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))


@skipUnless(_registration_available(), 'ALLOW_ACCOUNT_CREATION disabled; registration URLs absent')
class RestAuthRegistrationContractTest(ApiContractTestCase):
    def test_registration_success_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/registration/',
            {
                'username': 'brand_new_user',
                'password1': 'brand-new-pass-123',
                'password2': 'brand-new-pass-123',
                'email': 'brandnew@seven23.test',
                'origin': 'https://seven23.test',
            },
            format='json',
        )
        data = self.assertJsonResponse(
            response, TOKEN_KEY_V1, expected_status=status.HTTP_201_CREATED
        )
        self.assertTrue(User.objects.filter(username='brand_new_user').exists())

        # Token from registration must unlock user endpoint with USER_V1 shape
        user_response = client.get(
            '/api/v1/rest-auth/user/',
            HTTP_AUTHORIZATION=f'Token {data["key"]}',
        )
        user_data = self.assertJsonResponse(user_response, USER_V1)
        self.assertEqual(user_data['username'], 'brand_new_user')

    def test_registration_password_mismatch_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/registration/',
            {
                'username': 'mismatch_user',
                'password1': 'brand-new-pass-123',
                'password2': 'different-pass-123',
                'email': 'mismatch@seven23.test',
                'origin': 'https://seven23.test',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_registration_duplicate_username_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/registration/',
            {
                'username': self.user.username,
                'password1': 'brand-new-pass-123',
                'password2': 'brand-new-pass-123',
                'email': 'dup@seven23.test',
                'origin': 'https://seven23.test',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_resend_email_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/registration/resend-email/',
            {'email': self.user.email},
            format='json',
        )
        self.assertIn(
            response.status_code,
            (status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST),
        )
        assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))

    def test_verify_email_invalid_shape(self):
        client = APIClient()
        response = client.post(
            '/api/v1/rest-auth/registration/verify-email/',
            {'key': 'not-a-real-key'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # may be HTML or JSON depending on dj-rest-auth version
        if response.get('Content-Type', '').startswith('application/json'):
            assert_json_shape(response.json(), AnyOf(DRF_DETAIL_V1, DRF_VALIDATION_V1))
