"""
    Tests Account API
"""
from django.test import TransactionTestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from django_723e.models.currency.models import Currency

class ApiCurrenciesTest(TransactionTestCase):
    """ Account retrieve """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='foo')
        self.usd = Currency.objects.create(name=u"US Dollars", sign="USD")
        self.eur = Currency.objects.create(name=u"Euro", sign="EUR")

    def test_currencies_retrieve(self):
        """
            Verify only related user can access data
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/currencies')
        data = response.json()
        # Verify data structure
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 2

        # Verify permission
        response = self.client.get('/api/v1/currencies/%d' % self.usd.id)
        assert response.status_code == status.HTTP_200_OK
        response = self.client.get('/api/v1/currencies/%d' % self.eur.id)
        assert response.status_code == status.HTTP_200_OK
        response = self.client.get('/api/v1/currencies/999999')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_currencies_put(self):
        """
            We try to edit an account object
        """
        response = self.client.put('/api/v1/currencies/%d' % self.eur.id,
                                   {'name': "New Euro",
                                    'sign': self.eur.sign,
                                   })
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_currencies_post(self):
        """
            We try to edit an account object
        """
        response = self.client.post('/api/v1/currencies',
                                    {'name': 'Ether',
                                     'sign': 'ETH',
                                    })
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_currencies_destroy(self):
        """
            We try to edit an account object
        """
        response = self.client.delete('/api/v1/currencies/%d' % self.eur.id)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
