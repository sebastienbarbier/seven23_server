# -*- coding: utf-8 -*-
"""
    Testing categories modules
"""
from django.test import TransactionTestCase
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User

from seven23.models.accounts.models import Account
from seven23.models.currency.models import Currency
from seven23.models.categories.models import Category
from seven23.models.transactions.models import DebitsCredits

class CategoriesTest(TransactionTestCase):
    """
        Test categories
    """

    def setUp(self):

        self.user = User.objects.create()
        self.user.login = "foo"
        self.user.save()

        self.euro = Currency.objects.create(name="Euro",
                                            sign=u"\u20AC",
                                            space=True,
                                            after_amount=True)
        self.chf = Currency.objects.create(name="Franc suisse", sign="CHF")
        self.thb = Currency.objects.create(name=u"Bahts Thaïlandais", sign="BHT")

        self.account = Account.objects.create(name="Compte courant",
                                              currency=self.euro,
                                              owner=self.user)
        self.cat1 = Category.objects.create(account=self.account, blob="Category 1")
        self.cat2 = Category.objects.create(account=self.account, blob="Category 2")

    def test_categories_delete(self):
        """
            Try to delete a Category. If it has transaction, is just disable to keep trace,
            and if not, is delete.
        """
        trans1 = DebitsCredits.objects.create(account=self.account, blob="Shopping", category=self.cat1)
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
