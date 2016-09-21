# -*- coding: utf-8 -*-

from django.test import TransactionTestCase
from django.contrib.auth.models import User

from django_723e.models.accounts.models import Account
from django_723e.models.currency.models import Currency
from django_723e.models.categories.models import Category
from django_723e.models.transactions.models import DebitsCredits
import datetime

class AccountTest(TransactionTestCase):

    def setUp(self):
        """
            Create a user
        """
        self.user = User.objects.create()
        self.user.login = "foo"
        self.user.save()
        self.euro = Currency.objects.create(name="Euro", sign=u"\u20AC", space=True, after_amount=True)
        self.chf = Currency.objects.create(name="Franc suisse", sign="CHF")
        self.thb = Currency.objects.create(name=u"Bahts Thaïlandais", sign="BHT")

        self.account = Account.objects.create(user=self.user, name="Compte courant", currency=self.euro)
        self.cat1 = Category.objects.create(user=self.user, name="Category 1")
        self.cat2 = Category.objects.create(user=self.user, name="Category 2")

    def test_CategoriesMoveRight(self):
        """
            Create sub-categories and try to move them from one level up.
        """
        # Check is move_children_right properly moved children's category one level up.
        self.cat1_1 = Category.objects.create(user=self.user, name="Category 1.1", parent=self.cat1)
        self.cat1_2 = Category.objects.create(user=self.user, name="Category 1.2", parent=self.cat1)
        self.cat1.move_children_right()
        self.assertEqual(self.cat1.get_children().count(), 0)

        # Check if disabled function properly moved children's category one level up.
        self.cat1_1.parent = self.cat1
        self.cat1_1.save()
        self.cat1_2.parent = self.cat1
        self.cat1_2.save()
        self.cat1.disable()
        self.assertEqual(self.cat1.get_children().count(), 0)


    def test_CategoriesDelete(self):
        """
            Try to delete a Category. If it has transaction, is just disable to keep trace, and if not, is delete.
        """
        trans1 = DebitsCredits.objects.create(account=self.account,
                                            name="Shopping",
                                            local_amount=1,
                                            local_currency=self.euro,
                                            category=self.cat1)
        self.cat1.delete()
        self.assertEqual(self.cat1.active, False)

        trans1.delete()
        self.assertEqual(self.cat1.transactions.all().count(), 0)

        self.cat1.delete()
        self.assertEqual(Category.objects.all().count(), 1)


