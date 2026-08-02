"""Contract tests for /api/v1/users/* and /api/v1/user/delete."""

from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from seven23.tests.contracts.v1.base import ApiContractTestCase
from seven23.tests.contracts.v1.schemas import USER_V1


class UsersEmailContractTest(ApiContractTestCase):
    def setUp(self):
        super().setUp()
        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            primary=True,
            verified=False,
        )

    def test_email_update_success_shape(self):
        response = self.client.post(
            '/api/v1/users/email',
            {'email': 'updated@seven23.test'},
            format='json',
        )
        data = self.assertJsonResponse(response, USER_V1)
        self.assertEqual(data['email'], 'updated@seven23.test')

    def test_email_update_invalid_syntax_status(self):
        # Validation only runs when an EmailAddress already exists for the user.
        response = self.client.post(
            '/api/v1/users/email',
            {'email': 'ThisIsNotAnEmail'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_update_unauthenticated_has_no_auth_gate(self):
        # Endpoint uses @api_view without IsAuthenticated — anonymous calls error
        # when touching request.user rather than returning 401.
        client = APIClient()
        response = client.post(
            '/api/v1/users/email',
            {'email': 'x@seven23.test'},
            format='json',
        )
        self.assertIn(
            response.status_code,
            (status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN),
        )


class UsersTokenContractTest(ApiContractTestCase):
    def test_revoke_token_success(self):
        self.assertTrue(Token.objects.filter(user=self.user).exists())
        response = self.client.delete('/api/v1/users/token')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_revoke_token_when_missing(self):
        Token.objects.filter(user=self.user).delete()
        response = self.client.delete('/api/v1/users/token')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_revoke_token_unauthenticated_has_no_auth_gate(self):
        client = APIClient()
        response = client.delete('/api/v1/users/token')
        # Anonymous user has no token → 404 from the view's lookup
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserDeleteContractTest(ApiContractTestCase):
    def test_delete_user_success(self):
        user_id = self.user.id
        response = self.client.delete(
            '/api/v1/user/delete',
            {'password': self.password},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(id=user_id).exists())

    def test_delete_user_wrong_password(self):
        response = self.client.delete(
            '/api/v1/user/delete',
            {'password': 'wrong-password'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(id=self.user.id).exists())

    def test_delete_user_unauthenticated_has_no_auth_gate(self):
        client = APIClient()
        response = client.delete(
            '/api/v1/user/delete',
            {'password': self.password},
            format='json',
        )
        # Anonymous authenticate() fails → 400 (not 401)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
