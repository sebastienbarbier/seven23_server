"""
    Tests Account API
"""
from django.test import TransactionTestCase
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework import status

from django_723e.models.accounts.models import Account, AccountGuests
from django_723e.models.categories.models import Category
from django_723e.models.transactions.models import DebitsCredits
from django_723e.models.currency.models import Currency

class ApiChangesTest(TransactionTestCase):
    """ Changes retrieve """
