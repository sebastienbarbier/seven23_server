# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django_723e.models.currency.models import Currency
from django_723e.models.accounts.models import Account
from django_723e.models.categories.models import Category
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from colorfield.fields import ColorField

import calendar
import datetime

def getExchangeRate(date, local_currency, account_currency):
    """
        This function return the exchangeRate between a local and a foreign currency
    """
    # Look for change object with X > Y
    list = Change.objects.filter(new_currency=local_currency, date__lte=date).order_by('-date')
    for change in list:
        if change.local_currency == account_currency:
            return change.exchange_rate()

    # Look for reverse change object like Y > X
    list = Change.objects.filter(local_currency=local_currency, date__lte=date).order_by('-date')
    for change in list:
        if change.new_currency == account_currency:
            return 1 / change.exchange_rate()

    return None


class AbstractTransaction(models.Model):
    """
        Money transaction.
    """
    account          = models.ForeignKey(Account, related_name='transactions')
    name             = models.CharField(_(u'Name'), max_length=255)
    local_amount     = models.FloatField(_(u'Amount'), null=False, blank=False, help_text=_(u"Credit and debit are represented by positive and negative value."))
    local_currency   = models.ForeignKey(Currency, related_name='transactions')
    date             = models.DateField(_(u'Date'), editable=True, default=timezone.now)
    active           = models.BooleanField(_(u'Enable'), default=True, help_text=_(u"A disabled transaction will be save as a draft and not use in any report."))
    category         = models.ForeignKey(Category, related_name='transactions', blank=True, null=True)

    def __unicode__(self):
        return u"(%d) %s %s" % (self.pk, self.name, self.local_currency.verbose(self.local_amount))

    def update_amount(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        self.update_amount(*args, **kwargs)
        super(AbstractTransaction, self).save(*args, **kwargs) # Call the "real" save() method

    def value(self):
        return self.local_currency.verbose(self.local_amount)

class DebitsCredits(AbstractTransaction):

    foreign_amount     = models.FloatField(_(u'Reference Amount'), null=True, blank=True, editable=False, help_text=_(u"Value based on account curency."))
    foreign_currency   = models.ForeignKey(Currency, null=True, blank=True)

    def update_amount(self, *args, **kwargs):
        # If same currency as acount, no calculation needed
        if self.local_currency == self.account.currency:
            self.foreign_currency = None
            self.foreign_amount   = self.local_amount
        else:
            self.foreign_currency = self.account.currency
            exchange_rate         = getExchangeRate(self.date, self.local_currency, self.account.currency)
            if exchange_rate:
                self.foreign_amount = float("{0:.2f}".format(self.local_amount/exchange_rate))
            else:
                self.foreign_amount = None

    def isForeignCurrency(self):
        return self.foreign_currency and self.local_currency != self.foreign_currency

    def save(self, *args, **kwargs):
        self.update_amount(*args, **kwargs)
        super(AbstractTransaction, self).save(*args, **kwargs) # Call the "real" save() method

    def __unicode__(self):
        return u"%s" % (self.name)

class Change(AbstractTransaction):
    """
        Change money in a new currency.
    """
    new_amount   = models.FloatField(_(u'New Amount'), null=False, blank=False, help_text=_(u"Amount of cash in the new currency"))
    new_currency = models.ForeignKey(Currency, related_name="change", blank= True, null= True)

    def update_debitscredits(self):
        # Select closest same change pattern
        c = Change.objects.filter(account=self.account, date__gt=self.date, local_currency=self.local_currency, new_currency=self.new_currency).order_by("-date");
        # Select all debitsCredits transaction between this and newest one which no longer need to be updated
        if len(c) > 0:
            change = c[0]
            # Update reference_amount based on this new Change value
            list_debitscredits = DebitsCredits.objects.filter(account=self.account, date__gte=self.date, date__lt=change.date);
            for d in list_debitscredits:
                d.save()
        else:
            list_debitscredits = DebitsCredits.objects.filter(account=self.account, date__gte=self.date);
            for d in list_debitscredits:
                d.save()

    def __unicode__(self):
        return u"%d %s (%s -> %s)" % (self.pk, self.name, self.local_currency.verbose(self.amount), self.new_currency.verbose(self.new_amount))

    def force_save(self, *args, **kwargs):
        super(Change, self).save(*args, **kwargs) # Call the "real" save() method

    def save(self, *args, **kwargs):
        # First save to have correct value
        super(Change, self).save(*args, **kwargs) # Call the "real" save() method
        self.update_debitscredits()

    def delete(self, *args, **kwargs):
        super(Change, self).delete(*args, **kwargs) # Call the "real" save() method

    def exchange_rate(self):
        return float(self.new_amount) / float(self.local_amount)

    def new_value(self):
        return self.new_currency.verbose(self.new_amount)
