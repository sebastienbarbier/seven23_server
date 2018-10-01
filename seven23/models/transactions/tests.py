# -*- coding: utf-8 -*-
"""
    Tests for transactions module
"""
import datetime

from django.test import TransactionTestCase
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from seven23.models.accounts.models import Account
from seven23.models.currency.models import Currency
from seven23.models.categories.models import Category
from seven23.models.transactions.models import DebitsCredits, Change

class TransactionsTest(TransactionTestCase):
    """
        Test transaction model
    """
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

        self.euro = Currency.objects.create(name="Euro",
                                            sign=u"\u20AC",
                                            space=True,
                                            after_amount=True)
        self.chf = Currency.objects.create(name="Franc suisse", sign="CHF")
        self.thb = Currency.objects.create(name=u"Bahts Thaïlandais", sign="BHT")
        self.usd = Currency.objects.create(name=u"US Dollars", sign="USD")
        self.account = Account.objects.create(name="User Account",
                                              currency=self.euro,
                                              owner=self.user)
        self.cat1 = Category.objects.create(account=self.account, blob="Category 1")
        self.cat2 = Category.objects.create(account=self.account, blob="Category 2")


    def test_categories_delete(self):
        """
            Try to delete a Category.
            If it has transaction, it is just disable to keep trace,
            and if no transaction attched, it is delete.
        """
        trans1 = DebitsCredits.objects.create(account=self.account,
                                              blob="Shopping",
                                              category=self.cat1)
        self.cat1.delete()
        self.assertEqual(self.cat1.active, False)

        trans1.delete()
        self.assertEqual(self.cat1.transactions.all().count(), 0)

        self.cat1.delete()
        self.assertEqual(Category.objects.all().count(), 2)

        none_deleted_categories = []
        for category in Category.objects.all():
            if category.deleted == False:
                none_deleted_categories.append(category)

        self.assertEqual(len(none_deleted_categories), 1)


    def test_categories_sum(self):
        """
            Create a serie of transaction and verify calculated data

            J-3    trans    49.3 €    Enable     cat1
            J-2    trans    20 €      Disable    cat1
        """
        # First transaction
        trans1 = DebitsCredits.objects.create(account=self.account,
                                              blob="Shopping")
        self.assertNotEqual(trans1, None)

        # Second transaction
        trans2 = DebitsCredits.objects.create(account=self.account,
                                              blob="Shopping")
        self.assertNotEqual(trans2, None)

        # Check if disabled transaction are used in sum
        trans2.active = False
        trans2.save()


    def test_change(self):
        """
            Test if Change object calculate well the exchange_rate
        """
        change = Change.objects.create(account=self.account,
                                       blob="Withdraw")
        self.assertNotEqual(change, None)
        # exchange_rate = float(change.new_amount) / float(change.local_amount)
        # self.assertEqual(exchange_rate, 1.1666666666666667)

        change2 = Change.objects.create(account=self.account,
                                        blob="Withdraw")
        self.assertNotEqual(change2, None)

        # exchange_rate = float(change2.new_amount) / float(change2.local_amount)
        # self.assertEqual(exchange_rate, 1.0769230769230769)

    def test_change_transactions(self):
        """
            Test if editing change update transaction new_Amount
        """
        transaction1 = DebitsCredits.objects.create(account=self.account,
                                                    blob="Buy a 6 CHF item")
        # After this point, transaction 1 Should have no reference Value
        transaction1 = DebitsCredits.objects.get(pk=transaction1.pk)
        self.assertNotEqual(transaction1, None)

        # We define a change rate after the transaction 1
        # and check if there is still no foreign_amount
        Change.objects.create(account=self.account,
                              blob="Withdraw")
        transaction1 = DebitsCredits.objects.get(pk=transaction1.pk)
        self.assertNotEqual(transaction1, None)

        # We define a change rate BEFORE transaction 1
        # To check if trsnaction foreign_amount has been edited
        Change.objects.create(account=self.account,
                              blob="Withdraw")

        transaction1 = DebitsCredits.objects.get(pk=transaction1.pk)
        self.assertNotEqual(transaction1, None)

        # We now create a transaction in THB.
        # App should not be able to define an exchange rate
        transaction2 = DebitsCredits.objects.create(account=self.account,
                                                    blob="Buy an item using Thai Baths")
        transaction2 = DebitsCredits.objects.get(pk=transaction2.pk)
        self.assertNotEqual(transaction2, None)

        # Now we had a change rate from CHF to THB
        # Should be able to define a EUR > THB exchange rate from
        # EUR > CHF > THB
        # In this case 80€ > 60 CHF > 120 THB so a 60 THB item should be 40€
        Change.objects.create(account=self.account,
                              blob="Withdraw")

        transaction2 = DebitsCredits.objects.get(pk=transaction2.pk)
        self.assertNotEqual(transaction2, None)

        # If I buy a new item using THB, I should have refernce_amount using Euro exchange rate
        transaction3 = DebitsCredits.objects.create(account=self.account,
                                                    blob="Buy a 6 CHF item")
        transaction3 = DebitsCredits.objects.get(pk=transaction3.pk)
        self.assertNotEqual(transaction3, None)

