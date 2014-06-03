# -*- coding: utf-8 -*-

from django.test import TransactionTestCase

from django_723e.models.currency.models import Currency

class CurrencyTest(TransactionTestCase):

        
    def test_CurrencyCreation(self):
        """
            Create sub-categories and try to move them from one level up.
        """
        # Check is move_children_right properly moved children's category one level up.
        self.euro = Currency.objects.create(name="Euro", sign="€", space=True, after_amount=True)
        self.chf = Currency.objects.create(name="Franc suisse", sign="CHF")
        self.assertNotEqual(self.euro, None)
        self.assertNotEqual(self.chf, None)


