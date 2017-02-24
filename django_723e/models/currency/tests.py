# -*- coding: utf-8 -*-
"""
    Test currency
"""
from django.test import TransactionTestCase
from django_723e.models.currency.models import Currency

class CurrencyTest(TransactionTestCase):
    """
        Testing currency model objects
    """
    def test_currency_creation(self):
        """
            Create sub-categories and try to move them from one level up.
            Check is move_children_right properly moved children's category one level up.
        """
        euro = Currency.objects.create(name="Euro", sign="€", space=True, after_amount=True)
        chf = Currency.objects.create(name="Franc suisse", sign="CHF")
        self.assertNotEqual(euro, None)
        self.assertNotEqual(chf, None)
