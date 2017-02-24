"""
    Tests Account API
"""
from django.test import TransactionTestCase
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from django_723e.models.accounts.models import Account
from django_723e.models.currency.models import Currency

class ApiAccountTest(TransactionTestCase):
    """ Account retrieve """

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create_user(username='foo', email='old@723e.com')
        self.user2 = User.objects.create_user(username='foo2')

        self.usd = Currency.objects.create(name=u"US Dollars", sign="USD")
        self.account = Account.objects.create(owner=self.user,
                                              name="Private Account",
                                              currency=self.usd)

        self.account2 = Account.objects.create(owner=self.user2,
                                               name="Private Account 2",
                                               currency=self.usd)

    def test_account_retrieve(self):
        """
            Verify only related user can access data
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/accounts')
        data = response.json()
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1
        assert data[0]['id'] == self.account.id
        assert data[0]['name'] == self.account.name
        assert data[0]['currency'] == self.usd.id

        # Verify permission
        response = self.client.get('/api/v1/accounts/%d' % self.account.id)
        assert response.status_code == status.HTTP_200_OK
        response = self.client.get('/api/v1/accounts/%d' % self.account2.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/v1/accounts')
        assert response.status_code == status.HTTP_200_OK
        response = self.client.get('/api/v1/accounts/%d' % self.account2.id)
        assert response.status_code == status.HTTP_200_OK
        response = self.client.get('/api/v1/accounts/%d' % self.account.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_account_put(self):
        """
            We try to edit an account object
        """
        self.client.force_authenticate(user=self.user)
        assert self.account.name == "Private Account"
        self.account.name = "Public Account"
        response = self.client.put('/api/v1/accounts/%d' % self.account.id,
                                   {'name': self.account.name,
                                    'currency': self.account.currency.id,
                                   })
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['name'] == "Public Account"

        response = self.client.get('/api/v1/accounts/%d' % self.account.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['name'] == "Public Account"

        response = self.client.put('/api/v1/accounts/%d' % self.account2.id,
                                   {'name': self.account2.name,
                                    'currency': self.account2.currency.id,
                                   })
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_account_post(self):
        """
            We try to edit an account object
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/accounts',
                                    {'name': 'Test creation',
                                     'currency': self.usd.id,
                                    })
        assert response.status_code == status.HTTP_201_CREATED

        response = self.client.get('/api/v1/accounts/%d' % response.json()['id'])
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['name'] == 'Test creation'

    def test_account_destroy(self):
        """
            We try to edit an account object
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('/api/v1/accounts/%d' % self.account.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = self.client.get('/api/v1/accounts/%d' % self.account.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = self.client.get('/api/v1/accounts/%d' % self.account2.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = self.client.delete('/api/v1/accounts/%d' % self.account2.id)
        assert response.status_code == status.HTTP_404_NOT_FOUND


