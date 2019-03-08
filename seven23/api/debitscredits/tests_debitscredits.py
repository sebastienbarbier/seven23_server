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
                                                blob='Category 1')

        self.user2 = User.objects.create_user(username='foo2')
        self.account2 = Account.objects.create(owner=self.user2,
                                               name="Private Account 2",
                                               currency=self.usd)

        self.category2 = Category.objects.create(account=self.account2,
                                                 blob='Category 2')

        DebitsCredits.objects.create(account=self.account,
                                     blob='Spending')

        DebitsCredits.objects.create(account=self.account,
                                     blob='Spending2')

        DebitsCredits.objects.create(account=self.account2,
                                     blob='Spending')


    def test_debitscredits_retrieve(self):
        """
            Retrieve data with a user owning an account and being gest in an other one.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/debitscredits')
        data = response.json()
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 2
        assert data[0]['blob'] == 'Spending'

        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/v1/debitscredits')
        data = response.json()
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1
        assert data[0]['blob'] == 'Spending'

        response = self.client.get('/api/v1/categories')
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

        AccountGuests.objects.create(account=self.account2,
                                     user=self.user,
                                     permissions='W')

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/debitscredits')
        assert len(response.json()) == 3

        self.client.force_authenticate(user=self.user2)
        response = self.client.get('/api/v1/debitscredits')
        assert len(response.json()) == 1

        # Test POST request
        self.client.post('/api/v1/debitscredits', {
            'account': self.account2.id,
            'blob': 'Spending Again 2'
        }, format='json')

        response = self.client.get('/api/v1/debitscredits')
        assert len(response.json()) == 2

        # Test PUT request
        item = response.json()[0]
        assert item['blob'] == 'Spending'

        item['blob'] = 'New Blob'

        res = self.client.put('/api/v1/debitscredits/' + str(item['id']), item)

        response = self.client.get('/api/v1/debitscredits')
        assert response.json()[0]['blob'] == 'New Blob'

    def test_debitscredits_bulk(self):
        """
            Retrieve data with a user owning an account and being gest in an other one.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/v1/debitscredits')
        data = response.json()
        assert len(response.json()) == 2

        response = self.client.post('/api/v1/debitscredits', {
            'account': self.account.id,
            'blob': 'Spending Again'
        }, format='json')
        data = response.json()

        response = self.client.get('/api/v1/debitscredits')
        data = response.json()
        assert len(response.json()) == 3

        response = self.client.post('/api/v1/debitscredits', [{
            'account': self.account.id,
            'blob': 'Spending Again 2'
        }, {
            'account': self.account.id,
            'blob': 'Spending Again 3'
        }], format='json')
        created_data = response.json()

        response = self.client.get('/api/v1/debitscredits')
        data = response.json()
        assert len(response.json()) == 5

        edited_item = data[0]
        edited_item2 = data[1]

        # Test bulk patch request
        self.client.patch('/api/v1/debitscredits', [{'id': edited_item['id'], 'blob': 'Edited blob'}, {'id': edited_item2['id'], 'blob': 'Edited blob'}], format='json')

        response = self.client.get('/api/v1/debitscredits/' + str(edited_item['id']))
        data = response.json()

        assert edited_item['blob'] != 'Edited blob'
        assert data['blob'] == 'Edited blob'

        response = self.client.get('/api/v1/debitscredits/' + str(edited_item2['id']))
        data = response.json()

        assert edited_item2['blob'] != 'Edited blob'
        assert data['blob'] == 'Edited blob'


    def test_debitscredits_since_last_edited(self):
        """
            Retrieve data with a user owning an account and being gest in an other one.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/debitscredits')
        data = response.json()

        minDate = datetime.datetime.now()
        for transaction in data:
            if datetime.datetime.strptime(transaction['last_edited'], '%Y-%m-%dT%H:%M:%S.%fZ') < minDate:
                minDate = datetime.datetime.strptime(transaction['last_edited'], '%Y-%m-%dT%H:%M:%S.%fZ')

        response = self.client.get('/api/v1/debitscredits?last_edited=%s' % minDate)
        data = response.json()
        assert len(response.json()) == 1