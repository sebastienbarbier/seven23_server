# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django_723e.models.currency.models import Currency
from django_723e.models.accounts.models import Account
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django_723e.models.transactions.utils import recalculateAllTransactionsAfterChange
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from colorfield.fields import ColorField

import calendar
import datetime

class Category(MPTTModel):
    """
        Category of transaction.
    """
    user        = models.ForeignKey(User, related_name='categories')
    name        = models.CharField(_(u'Name'), max_length=128)
    description = models.TextField(_(u'Description'))
    color       = ColorField(default='ffffff')
    icon        = models.TextField(_(u'Icon'))
    parent      = TreeForeignKey('self', null=True, blank=True, related_name='children')
    selectable  = models.BooleanField(_(u'Selectable'), default=True, help_text=_(u"Can be link to a transaction"))
    active      = models.BooleanField(_(u'Enable'), default=True, help_text=_(u"Delete a category only disable it"))

    def __unicode__(self):
        return u'%s' % (self.name)

    class MPTTMeta:
        order_insertion_by = ['name']

    def move_children_right(self):
        """ Move direct children categories to same level """
        if self.get_children():
            for i in self.get_children():
                i.move_to(self, 'right')
                i.save()

    def enable(self):
        self.active = True
        self.save()

    def disable(self):
        self.move_children_right()
        self.active = False
        self.save()

    def toggle(self):
        if self.active:
            self.disable()
        else:
            self.enable()

    def delete(self):
        """
            If a category object is link to a transaction, it cannot be delete because
            we need to keep trace of all transactions. It is only disable/hide.
        """
        self.move_children_right()
        if self.transactions.all():
            self.toggle()
        else:
            super(Category, self).delete()

    def sum(self, year=None, month=None, day=None):
        """
            Sum of transaction in this category
            Return None if no value
        """
        if not year:
            return self.sum_between()

        if not month:
            return self.sum_between(datetime.date(year, 1, 1), datetime.date(year, 12, 31))

        if not day:
            return self.sum_between(datetime.date(year, month, 1), datetime.date(year, month, calendar.monthrange(year, month)[1]))

        return self.sum_between(datetime.date(year, month, day), datetime.date(year, month, day))

    def sum_between(self, date1=None, date2=None):
        """
            Sum of current transaction between date1 and date2. date1 < date2.
            Return None if no value
        """
        if date1 > date2:
            date1, date2 = date2, date1

        return AbstractTransaction.objects.filter(date__gte=date1, date__lte=date2, active=True, category__exact=self).aggregate(Sum('amount'))['amount__sum']


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
            list_change = Change.objects.filter(new_currency=self.currency, date__lte=self.date).order_by('date')
            if list_change:
                change = list_change[0]
                self.reference_amount = self.amount/change.exchange_rate()
            else:
                self.reference_amount = None

    def save(self, *args, **kwargs):
        self.update_amount()
        super(AbstractTransaction, self).save(*args, **kwargs) # Call the "real" save() method

    def value(self):
        return self.currency.verbose(self.amount)


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

        super(Change, self).save(*args, **kwargs) # Call the "real" save() method

    def exchange_rate(self):
        return self.new_amount / self.amount

    def new_value(self):
        return self.new_currency.verbose(self.new_amount)


