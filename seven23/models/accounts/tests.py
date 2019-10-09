# -*- coding: utf-8 -*-
"""
    Tests for accounts module

"""
from django.test import TransactionTestCase
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User

from seven23.models.accounts.models import Account, AccountGuests
from seven23.models.currency.models import Currency
from seven23.models.categories.models import Category
from seven23.models.transactions.models import DebitsCredits, Change

class AccountTest(TransactionTestCase):
    """ Account test """

    def setUp(self):
        """
            Create a set of data to access during tests
            user foo
            currency euro, chf, thb
            account user.foo.account
            categories category1, category2
        """
        self.user = User.objects.create()
        self.user.username = "foo"
        self.user.save()

        self.euro = Currency.objects.create(
            name="Euro", sign=u"\u20AC", space=True, after_amount=True)
        self.chf = Currency.objects.create(name="Franc suisse", sign="CHF")
        self.thb = Currency.objects.create(name=u"Bahts Thaïlandais", sign="BHT")
        self.usd = Currency.objects.create(name=u"US Dollars", sign="USD")
        self.account = Account.objects.create(owner=self.user,
                                              name="Compte courant",
                                              currency=self.euro)
        self.cat1 = Category.objects.create(account=self.account, blob="Category 1")
        self.cat2 = Category.objects.create(account=self.account, blob="Category 2")

    def test_create_account(self):
        """
            Create a profile, and a standard account in euro currency.
        """
        self.assertNotEqual(self.account, None)
        AccountGuests.objects.create(account=self.account, user=self.user, permissions='A')
        self.assertEqual(len(self.account.guests.all()), 1)