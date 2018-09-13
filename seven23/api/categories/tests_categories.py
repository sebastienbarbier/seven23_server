"""
    Tests Account API
"""
import json

from django.test import TransactionTestCase
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from seven23.models.accounts.models import Account, AccountGuests
from seven23.models.categories.models import Category
from seven23.models.transactions.models import DebitsCredits
from seven23.models.currency.models import Currency

class ApiCategoryTest(TransactionTestCase):
    """ Account retrieve """

    def setUp(self):

        self.client = APIClient()

        self.usd = Currency.objects.create(name=u"US Dollars", sign="USD")

        self.user = User.objects.create_user(username='foo', email='old@723e.com')
        self.account = Account.objects.create(owner=self.user,
                                              name="Private Account",
                                              currency=self.usd)

        blob1 = { 'name': 'Category 2' }
        self.category = Category.objects.create(account=self.account,
                                                blob=json.dumps(blob1))

        self.user2 = User.objects.create_user(username='foo2')
        self.account2 = Account.objects.create(owner=self.user2,
                                               name="Private Account 2",
                                               currency=self.usd)

        blob2 = { 'name': 'Category 2' }
        self.category2 = Category.objects.create(account=self.account2,
                                                 blob=json.dumps(blob2))

        DebitsCredits.objects.create(account=self.account,
                                     blob='sadkjhfgsdaf')

        DebitsCredits.objects.create(account=self.account2,
                                     blob='sadkjhfgsdaf')

    def test_categories_retrieve(self):
        """
            Retrieve data with a user owning an account and being gest in an other one.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/categories')
        data = response.json()
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1

        AccountGuests.objects.create(account=self.account2,
                                     user=self.user,
                                     permissions='W')

        response = self.client.get('/api/v1/categories')
        data = response.json()
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 2

    def test_categories_post(self):
        """
            We try to create a new category object
        """

        blob = { 'name': 'Category post' }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/categories',
                                    {'account': self.account.id,
                                     'blob': json.dumps(blob)
                                    })
        assert response.status_code == status.HTTP_201_CREATED

        response = self.client.post('/api/v1/categories',
                                    {'account':self.account2.id,
                                     'blob': json.dumps(blob)
                                    })
        assert response.status_code == status.HTTP_201_CREATED


    # def test_categories_delete(self):
    #     """
    #         Retrieve data with a user owning an account and being gest in an other one.
    #     """
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.delete('/api/v1/categories/%d' % self.category.id)
    #     print(response)
    #     data = response.json()
    #     # Verify data structure
    #     assert response.status_code == status.HTTP_200_OK
