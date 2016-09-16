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
                                            currency=self.euro,
                                            name="Shopping",
                                            amount=1,
                                            category=self.cat1)
        self.cat1.delete()
        self.assertEqual(self.cat1.active, False)

        trans1.delete()
        self.assertEqual(self.cat1.transactions.all().count(), 0)

        self.cat1.delete()
        self.assertEqual(Category.objects.all().count(), 1)


    def test_CategoriesSum(self):
        """
            Create a serie of transaction and verify calculated data

            J-3    trans    49.3    Enable     cat1
            J-2    trans    20      Disable    cat1
        """
        # First transaction
        trans1 = DebitsCredits.objects.create(account=self.account,
                                            currency=self.euro,
                                            date=datetime.date.today() - datetime.timedelta(days=3),
                                            name="Shopping",
                                            amount=49.3,
                                            category=self.cat1)
        self.assertNotEqual(trans1, None)

        # Second transaction
        trans2 = DebitsCredits.objects.create(account=self.account,
                                            currency=self.euro,
                                            date=datetime.date.today() - datetime.timedelta(days=2),
                                            name="Shopping",
                                            amount=20,
                                            category=self.cat1)
        self.assertNotEqual(trans2, None)

        # Check if disabled transaction are used in sum
        self.assertEqual(self.cat1.sum_between(datetime.date.today(), datetime.date.today()-datetime.timedelta(days=3)), 69.3)

        # Check if disabled transaction are used in sum
        trans2.active = False
        trans2.save()
        self.assertEqual(self.cat1.sum_between(datetime.date.today(), datetime.date.today()-datetime.timedelta(days=3)), 49.3)



    def test_Change(self):

        change = Change.objects.create(account=self.account,
                                       currency=self.euro,
                                       date=datetime.datetime.today() - datetime.timedelta(days=1),
                                       name="Change",
                                       amount=120,
                                       new_amount=140,
                                       new_currency=self.chf)
        self.assertNotEqual(change, None)
        self.assertEqual(change.exchange_rate(), 1.00)

    def test_Change_Transactions(self):
        trans1 = DebitsCredits.objects.create(account=self.account,
                                            currency=self.chf,
                                            date=datetime.datetime.today() - datetime.timedelta(days=20),
                                            name="Achat 1 en suisse",
                                            amount=6)
        # self.assertEqual(trans1.reference_value(), None)
        change1 = Change.objects.create(account=self.account,
                                       date=datetime.datetime.today() - datetime.timedelta(days=30),
                                       name="Change",
                                       amount=80,
                                       currency=self.euro,
                                       new_amount=60,
                                       new_currency=self.chf)

        change1 = Change.objects.get(pk=change1.pk)
        # self.assertEqual(trans1.reference_value(), 8)
        # self.assertEqual(change1.balance, 54) # Still 54 CHF Available
        change1.balance = 0
        change1.force_save()
        self.assertEqual(change1.balance, 0)
        #
        # TRY WITH MULTIPLE CHANGE ON A SINGLE TRANSACTION
        #



        trans2 = DebitsCredits.objects.create(account=self.account,
                                            currency=self.chf,
                                            date=datetime.datetime.today() - datetime.timedelta(days=2),
                                            name="Achat 1 en suisse",
                                            amount=60)

        # self.assertEqual(trans2.due_to_change(), 60) # Still 60 CHF to xhange
        # self.assertEqual(trans2.is_change_complete(), False)
        change2 = Change.objects.create(account=self.account,
                                       date=datetime.datetime.today().date() - datetime.timedelta(days=3),
                                       name="Change",
                                       amount=80,
                                       currency=self.euro,
                                       new_amount=40,
                                       new_currency=self.chf)
        change2 = Change.objects.get(pk=change2.pk)
        # self.assertEqual(change2.balance, 0)
        # self.assertEqual(trans2.is_change_complete(), False)
        # self.assertEqual(trans2.due_to_change(), 20) # Only 30 CHF to change now
        change3 = Change.objects.create(account=self.account,
                                       date=datetime.datetime.today().date() - datetime.timedelta(days=3),
                                       name="Change",
                                       amount=20,
                                       currency=self.euro,
                                       new_amount=40,
                                       new_currency=self.chf)

        change3 = Change.objects.get(pk=change3.pk)
        trans2 = DebitsCredits.objects.get(pk=trans2.pk)

        # self.assertEqual(trans2.due_to_change(), 0) # No more Money to Change
        # self.assertEqual(trans2.is_change_complete(), True) # No more Money to Change
        self.assertEqual(trans2.amount, 60)
        change3 = Change.objects.get(pk=change3.pk)
        # self.assertEqual(change3.balance, 20)
        # self.assertEqual(trans2.reference_value(), 90)


    def test_Change_Transactions3(self):
        Change.objects.create(account=self.account,
                                   date=datetime.datetime.today() - datetime.timedelta(days=3),
                                   name="Change",
                                   amount=80,
                                   currency=self.euro,
                                   new_amount=40,
                                   new_currency=self.chf)
        trans1 = DebitsCredits.objects.create(account=self.account,
                                            currency=self.chf,
                                            date=datetime.datetime.today() - datetime.timedelta(days=2),
                                            name="Achat 2 en suisse",
                                            amount=60)

        # self.assertEqual(trans1.reference_value(), None)
        # self.assertEqual(trans1.due_to_change(), 20)

        c2 = Change.objects.create(account=self.account,
                                   date=datetime.datetime.today() - datetime.timedelta(days=3),
                                   name="Change",
                                   amount=40,
                                   currency=self.euro,
                                   new_amount=40,
                                   new_currency=self.chf)
        c2 = Change.objects.get(pk=c2.pk)

        # self.assertEqual(c2.balance, 20)
        # self.assertEqual(trans1.reference_value(), 100)

        c2.delete()
        trans1 = DebitsCredits.objects.get(pk=trans1.pk)

        # self.assertEqual(trans1.reference_value(), None)
        # self.assertEqual(trans1.due_to_change(), 20)

        c3 = Change.objects.create(account=self.account,
                                   date=datetime.datetime.today() - datetime.timedelta(days=2),
                                   name="Change",
                                   amount=40,
                                   currency=self.euro,
                                   new_amount=40,
                                   new_currency=self.chf)
        c3 = Change.objects.get(pk=c3.pk)

        # self.assertEqual(c3.balance, 20)
        # self.assertEqual(trans1.reference_value(), 100)

    def test_Change_Delete_Transactions(self):
        c1 = Change.objects.create(account=self.account,
                                   date=datetime.datetime.today() - datetime.timedelta(days=5),
                                   name="Change",
                                   amount=80,
                                   currency=self.euro,
                                   new_amount=40,
                                   new_currency=self.chf)
        t1 = DebitsCredits.objects.create(account=self.account,
                                            currency=self.chf,
                                            date=datetime.datetime.today() - datetime.timedelta(days=2),
                                            name="Achat 2 en suisse",
                                            amount=60)
        c2 = Change.objects.create(account=self.account,
                                   date=datetime.datetime.today() - datetime.timedelta(days=4),
                                   name="Change",
                                   amount=40,
                                   currency=self.euro,
                                   new_amount=40,
                                   new_currency=self.chf)
        t2 = DebitsCredits.objects.create(account=self.account,
                                            currency=self.chf,
                                            date=datetime.datetime.today() - datetime.timedelta(days=2),
                                            name="Achat 2 en suisse",
                                            amount=60)
        c3 = Change.objects.create(account=self.account,
                                   date=datetime.datetime.today() - datetime.timedelta(days=3),
                                   name="Change",
                                   amount=120,
                                   currency=self.euro,
                                   new_amount=40,
                                   new_currency=self.chf)
        t3 = DebitsCredits.objects.create(account=self.account,
                                            currency=self.chf,
                                            date=datetime.datetime.today() - datetime.timedelta(days=2),
                                            name="Achat 2 en suisse",
                                            amount=40)
        t1 = DebitsCredits.objects.get(pk=t1.pk)
        t2 = DebitsCredits.objects.get(pk=t2.pk)
        t3 = DebitsCredits.objects.get(pk=t3.pk)

        # self.assertEqual(t1.is_change_complete(), True)
        # self.assertEqual(t1.reference_value(), 100)
        # self.assertEqual(t2.is_change_complete(), True)
        # self.assertEqual(t2.reference_value(), 140)
        # self.assertEqual(t3.is_change_complete(), False)
        # self.assertEqual(t3.reference_value(), None)

        t2.delete()

        t1 = DebitsCredits.objects.get(pk=t1.pk)
        t3 = DebitsCredits.objects.get(pk=t3.pk)


        # self.assertEqual(t1.is_change_complete(), True)
        # self.assertEqual(t1.reference_value(), 100)
        # self.assertEqual(t3.is_change_complete(), True)
        # self.assertEqual(t3.reference_value(), 80)


