# -*- coding: utf-8 -*-

from django.test import TransactionTestCase
from django.contrib.auth.models import User

from django_723e.models.currency.models import Currency
from django_723e.models.accounts.models import Account

class AccountTest(TransactionTestCase):
    
    def setUp(self):
        """
            Create a user 
        """
        self.user = User.objects.create()
        self.user.login = "foo"
        self.user.save()
        self.euro = Currency.objects.create(name="Euro", sign="€", space=True, after_amount=True)

        
    def test_createAccount(self):
        """
            Create a profile, and a standard account in euro currency.
        """
        self.account = Account.objects.create(user=self.user, name="Compte courant", currency=self.euro)
        self.assertNotEqual(self.account, None)
        