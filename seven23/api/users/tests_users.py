"""
    Tests Account API
"""
import datetime
from django.test import TransactionTestCase
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from rest_framework import status

from seven23.models.accounts.models import Account, AccountGuests
from seven23.models.categories.models import Category
from seven23.models.transactions.models import DebitsCredits
from seven23.models.currency.models import Currency


class ApiUsersTest(TransactionTestCase):
    """ Account retrieve """

    def setUp(self):
        self.client = APIClient()

    def test_registration_new_user(self):
        """
            Create a user using rest-auth and get auth key in response.
        """
        response = self.client.post('/api/v1/rest-auth/registration/', {
            'username': 'test',
            'password1': 'testtest',
            'password2': 'testtest',
            'email': 'test@sebastienbarbier.com',
            'origin': 'https://next.seven23.io',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        # Test if response data key is define, a string, and not empty or blank
        self.assertTrue('key' in data)

        # Verify user serializer is returning profile user
        response = self.client.get('/api/v1/rest-auth/user/', HTTP_AUTHORIZATION='Token ' + data['key'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # Test if response data key is define, a string, and not empty or blank
        self.assertTrue('username' in data)
        self.assertEqual(data['username'], 'test')
        self.assertTrue('profile' in data)
        self.assertTrue('avatar' in data['profile'])
        self.assertTrue('auto_sync' in data['profile'])
        self.assertTrue('social_networks' in data['profile'])
        self.assertFalse(data['profile']['auto_sync'])