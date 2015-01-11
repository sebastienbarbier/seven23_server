# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django_723e.models.currency.models import Currency
from django_723e.models.accounts.models import Account
from django_723e.models.categories.models import Category
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from colorfield.fields import ColorField

import calendar
import datetime


class AbstractTransaction(models.Model):
    """
        Money transaction.
    """
    account          = models.ForeignKey(Account, related_name='transactions')
    currency         = models.ForeignKey(Currency, related_name='transactions')
    name             = models.CharField(_(u'Name'), max_length=255)
    amount           = models.FloatField(_(u'Amount'), null=False, blank=False, help_text=_(u"Credit and debit are represented by positive and negative value."))
    reference_amount = models.FloatField(_(u'Reference Amount'), null=True, blank=True, editable=False, help_text=_(u"Value based on account curency."))
    date             = models.DateField(_(u'Date'), editable=True, default=datetime.date.today())
    active           = models.BooleanField(_(u'Enable'), default=True, help_text=_(u"A disabled transaction will be save as a draft and not use in any report."))
    category         = models.ForeignKey(Category, related_name='transactions', blank=True, null=True)

    def __unicode__(self):
        return u"(%d) %s %s" % (self.pk, self.name, self.currency.verbose(self.amount))

    def update_amount(self):
        if type(self) is not Change and self.currency is not self.account.currency:
            list_change = Change.objects.filter(new_currency=self.currency, date__lte=self.date).order_by('-date')
            if list_change:
                change = list_change[0]
                self.reference_amount = self.amount/change.exchange_rate()
            else:
                self.reference_amount = self.amount

    def save(self, *args, **kwargs):
        self.update_amount()
        super(AbstractTransaction, self).save(*args, **kwargs) # Call the "real" save() method

    def value(self):
        return self.currency.verbose(self.amount)

    def isForeignCurrency(self):
        return not self.currency == self.account.currency


class DebitsCredits(AbstractTransaction):

    def __unicode__(self):
        return u"%s" % (self.name)


class Cheque(AbstractTransaction):
    """
        A cheque is like a Transaction but with two differents dates :
            - When you write a cheque (transaction.date)
            - When it is debit from you bank account (cheque.debit_date)
    """
    cheque_name = models.CharField(_(u'Beneficiary'), max_length= 255, null=True, blank=True)
    place       = models.CharField(_(u'Localisation'), max_length= 255, null=True, blank=True)
    debit_date  = models.DateField(_(u'Debit date'), editable=True, null=True, blank=True)

class Tranfert(AbstractTransaction):
    """
        Money Transfert from one account to an other (one of yours or externe).
    """
    account_dest    = models.ForeignKey(Account, related_name='transfert')

    def __unicode__(self):
        return u"%s %s (%s -> %s)" % (self.name, self.currency.verbose(self.amount), self.account, self.account_dest)

class Change(AbstractTransaction):
    """
        Change money in a new currency.
    """
    new_amount   = models.FloatField(_(u'New Amount'), null=False, blank=False, help_text=_(u"Ammount of cash in the new currency"))
    new_currency = models.ForeignKey(Currency, related_name="change", blank= True, null= True)

    def __unicode__(self):
        return u"%d %s (%s -> %s) : %f" % (self.pk, self.name, self.currency.verbose(self.amount), self.new_currency.verbose(self.new_amount), self.balance)

    def force_save(self, *args, **kwargs):
        super(Change, self).save(*args, **kwargs) # Call the "real" save() method

    def save(self, *args, **kwargs):
        # First save to have correct value
        super(Change, self).save(*args, **kwargs) # Call the "real" save() method
        # Select nextChange plus récent que celui ci
        c = Change.objects.filter(date__gt=self.date, new_currency=self.new_currency).order_by("-date");
        # Select tous les Débits après self mais avant nextChange
        if len(c) > 0:
            change = c[0]
            #Update leur ratio ... ca semble judicieux !!!
            list_debitscredits = DebitsCredits.objects.filter(date__gte=self.date, date__lt=change.date);
            for d in list_debitscredits:
                d.update_amount()
                d.save()
        else:
            list_debitscredits = DebitsCredits.objects.filter(date__gte=self.date);
            for d in list_debitscredits:
                d.update_amount()
                d.save()


    def exchange_rate(self):
        return float("{0:.2f}".format(self.new_amount / self.amount))

    def new_value(self):
        return self.new_currency.verbose(self.new_amount)


