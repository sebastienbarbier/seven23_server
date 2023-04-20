# -*- coding: utf-8 -*-
"""
    Test currency
"""
import datetime
from django import forms
from django.utils import timezone
from django.test import TestCase
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User
from .forms import SuperUserForm
from django.conf import settings

class SuperUserFormTest(TestCase):
    """
        Testing currency model objects
    """
    def test_superuser_form(self):
        """
            Create sub-categories and try to move them from one level up.
            Check is move_children_right properly moved children's category one level up.
        """
        # Delete all users
        User.objects.all().delete()
        self.assertEqual(User.objects.count() == 0, True)

        response = self.client.post("/", {
            'username': 'test',
            'email': 'admin@seven23.io',
            'password': 'abcd'
        })

        self.assertEqual(User.objects.count() == 1, True)

        response = self.client.post("/", {
            'username': 'test',
            'email': 'admin@seven23.io',
            'password': 'abcd'
        })

        self.assertEqual(User.objects.count() == 1, True)

        try:
            form = SuperUserForm({
                'username': 'test',
                'email': 'admin@seven23.io',
                'password': 'abcd'
            })
            form.save()
            raise Exception('Should have raised a ValidationError')
        except forms.ValidationError as e:
            self.assertEqual(e.message, 'There is already a superuser')

        self.assertEqual(User.objects.count() == 1, True)