# -*- coding: utf-8 -*-
"""
    Test currency
"""
import datetime
from django.utils import timezone
from django.test import TransactionTestCase
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User

from django.conf import settings

class ProfileTest(TransactionTestCase):
    """
        Testing currency model objects
    """
    def test_profile_creation(self):
        """
            Create sub-categories and try to move them from one level up.
            Check is move_children_right properly moved children's category one level up.
        """
        self.user = User.objects.create()
        self.user.login = "foo"
        self.user.save()

        expected_date = timezone.now() + datetime.timedelta(days=settings.TRIAL_PERIOD)

        self.assertEqual(self.user.profile.valid_until > timezone.now(), True)
        self.assertEqual(self.user.profile.valid_until < expected_date, True)
        self.assertEqual(self.user.profile.auto_sync, True)
        self.assertEqual(self.user.profile.key_verified, False)

        self.user.profile.key_verified = True
        self.user.profile.save()
        self.assertEqual(self.user.profile.key_verified, True)

        # Verify if changing password set key_verified flag to False using signals
        self.user.password = "AnOtherLongPassword"
        self.user.save()
        self.assertEqual(self.user.profile.key_verified, False)