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
from seven23.models.transactions.models import DebitsCredits, Change
from seven23.models.currency.models import Currency

class ApiChangesTest(TransactionTestCase):
    """ Changes retrieve """

    def setUp(self):

        self.client = APIClient()

        self.usd = Currency.objects.create(name=u"US Dollars", sign="USD")

        self.user = User.objects.create_user(username='foo', email='old@723e.com')
        self.account = Account.objects.create(owner=self.user,
                                              name="Private Account",
                                              currency=self.usd)

        self.category = Category.objects.create(account=self.account,
                                                blob='asdukfjhrsgdv')

        self.user2 = User.objects.create_user(username='foo2')
        self.account2 = Account.objects.create(owner=self.user2,
                                               name="Private Account 2",
                                               currency=self.usd)

        self.category2 = Category.objects.create(account=self.account2,
                                                 blob='asdukfjhrsgdv')

        DebitsCredits.objects.create(account=self.account,
                                     blob='asdukfjhrsgdv')

        DebitsCredits.objects.create(account=self.account2,
                                     blob='asdukfjhrsgdv')

    def test_changes_retrieve(self):
        """
            Retrieve data with a user owning an account and being gest in an other one.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/changes')
        data = response.json()
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 0


    def test_changes_since_last_edited(self):
        """
            Retrieve data with a user owning an account and being gest in an other one.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/changes')
        data = response.json()

        minDate = datetime.datetime.now()
        for transaction in data:
            if datetime.datetime.strptime(transaction['last_edited'], '%Y-%m-%dT%H:%M:%S.%fZ') < minDate:
                minDate = datetime.datetime.strptime(transaction['last_edited'], '%Y-%m-%dT%H:%M:%S.%fZ')

        response = self.client.get('/api/v1/changes?last_edited=%s' % minDate)
        data = response.json()
        assert len(response.json()) == 0

        Change.objects.create(account=self.account,
                               blob='asdukfjhrsgdv')

        response = self.client.get('/api/v1/changes?last_edited=%s' % minDate)
        data = response.json()
        assert len(response.json()) == 1

        minDate = datetime.datetime.strptime(data[0]['last_edited'], '%Y-%m-%dT%H:%M:%S.%fZ')
        response = self.client.get('/api/v1/changes?last_edited=%s' % minDate)
        data = response.json()
        assert len(response.json()) == 0