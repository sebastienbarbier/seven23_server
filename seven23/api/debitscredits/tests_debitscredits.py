"""
    Tests Account API
"""
from django.test import TransactionTestCase
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from seven23.models.accounts.models import Account, AccountGuests
from seven23.models.categories.models import Category
from seven23.models.transactions.models import DebitsCredits
from seven23.models.currency.models import Currency

class ApiDebitsCreditsTest(TransactionTestCase):
    """ Account retrieve """

    def setUp(self):

        self.client = APIClient()

        self.usd = Currency.objects.create(name=u"US Dollars", sign="USD")

        self.user = User.objects.create_user(username='foo', email='old@723e.com')
        self.account = Account.objects.create(owner=self.user,
                                              name="Private Account",
                                              currency=self.usd)

        self.category = Category.objects.create(account=self.account,
                                                name='Category 1')

        self.user2 = User.objects.create_user(username='foo2')
        self.account2 = Account.objects.create(owner=self.user2,
                                               name="Private Account 2",
                                               currency=self.usd)

        self.category2 = Category.objects.create(account=self.account2,
                                                 name='Category 2')

        DebitsCredits.objects.create(account=self.account,
                                     name='Spending',
                                     local_amount=10,
                                     local_currency=self.usd)

        DebitsCredits.objects.create(account=self.account2,
                                     name='Spending',
                                     local_amount=20,
                                     local_currency=self.usd)


    def test_debitscredits_retrieve(self):
        """
            Retrieve data with a user owning an account and being gest in an other one.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/debitscredits')
        data = response.json()
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1
        assert data[0]['local_amount'] == 10

        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/v1/debitscredits')
        data = response.json()
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1
        assert data[0]['local_amount'] == 20

        response = self.client.get('/api/v1/categories')
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

        AccountGuests.objects.create(account=self.account2,
                                     user=self.user,
                                     permissions='W')

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/debitscredits')
        assert len(response.json()) == 2

        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/v1/debitscredits')
        assert len(response.json()) == 1
