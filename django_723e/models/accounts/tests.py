# -*- coding: utf-8 -*-

from django.test import TransactionTestCase
from django.contrib.auth.models import User

from django_723e.models.accounts.models import Account
from django_723e.models.currency.models import Currency
from django_723e.models.categories.models import Category
from django_723e.models.transactions.models import AbstractTransaction, DebitsCredits, Change
import datetime

class AccountTest(TransactionTestCase):

    def setUp(self):
        """
            Create a set of data to access during tests
            user foo
            currency euro, chf, thb
            account user.foo.account
            categories category1, category2
        """
        self.user = User.objects.create()
        self.user.login = "foo"
        self.user.save()

        self.euro = Currency.objects.create(name="Euro", sign=u"\u20AC", space=True, after_amount=True)
        self.chf = Currency.objects.create(name="Franc suisse", sign="CHF")
        self.thb = Currency.objects.create(name=u"Bahts Thaïlandais", sign="BHT")
        self.usd = Currency.objects.create(name=u"US Dollars", sign="USD")
        self.cat1 = Category.objects.create(user=self.user, name="Category 1")
        self.cat2 = Category.objects.create(user=self.user, name="Category 2")


    def test_createAccount(self):
        """
            Create a profile, and a standard account in euro currency.
        """
        self.account = Account.objects.create(user=self.user, name="Compte courant", currency=self.euro)
        self.assertNotEqual(self.account, None)

    def test_Change_Currency(self):
        """
            Test is changing an account currency propagate well to all transactions.
        """
        self.account = Account.objects.create(user=self.user, name="Compte courant", currency=self.euro)

        # Transaction in Eur will have no difference between amount and reference_amount
        transaction1 = DebitsCredits.objects.create(account=self.account,
                                            date=datetime.datetime.today() - datetime.timedelta(days=20),
                                            name="Buy a 6 EUR item",
                                            amount=6,
                                            currency=self.euro)
        # After this point, transaction 1 Should have no reference Value
        transaction1 = DebitsCredits.objects.get(pk=transaction1.pk)
        self.assertEqual(transaction1.amount, 6)
        self.assertEqual(transaction1.reference_amount, 6)

        # Now we had a Change rate before the transaction 1, and change the account currency
        Change.objects.create(account=self.account,
                               date=datetime.datetime.today() - datetime.timedelta(days=30),
                               name="Withdraw",
                               amount=6,
                               currency=self.euro,
                               new_amount=4,
                               new_currency=self.chf)

        self.account = Account.objects.get(pk=self.account.pk)
        self.account.currency = self.chf
        self.account.save()

        # After this point, transaction 1 Should have no reference Value
        transaction1 = DebitsCredits.objects.get(pk=transaction1.pk)
        self.assertEqual(transaction1.amount, 6)
        self.assertEqual(transaction1.reference_amount, 4)
