# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from django_723e.models.currency.models import Currency
from django.core import serializers

import datetime


class Account(models.Model):
    """
        An account is considere as a bank account. Name is just a label for the user interface.
    """
    user     = models.ForeignKey(User, related_name="accounts")
    name     = models.CharField(_(u'Name'), max_length=255)
    create   = models.DateField(_(u'Creation date'), auto_now=True, editable=False)
    currency = models.ForeignKey(Currency, related_name='accounts')
    archived = models.BooleanField(_(u'Is archived'), default=False)

    class Meta:
        ordering = ('user', 'create', 'name')
        verbose_name = _(u'Account')

    def __unicode__(self):
        return u'%s' % (self.name)
