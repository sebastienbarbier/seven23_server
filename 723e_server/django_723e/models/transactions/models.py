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
    account     = models.ForeignKey(Account, related_name='transactions')
    currency    = models.ForeignKey(Currency, related_name='transactions')
    name        = models.CharField(_(u'Name'), max_length=255)
    amount      = models.FloatField(_(u'Amount'), null=False, blank=False, help_text=_(u"Credit and debit are represented by positive and negative value."))
    date        = models.DateField(_(u'Date'), editable=True, default=datetime.date.today())
    active      = models.BooleanField(_(u'Enable'), default=True, help_text=_(u"A disabled transaction will be save as a draft and not use in any report."))
    category    = models.ForeignKey(Category, related_name='transactions', blank=True, null=True)

    def __unicode__(self):
        return u"(%d) %s %s" % (self.pk, self.name, self.currency.verbose(self.amount))

    def save(self, *args, **kwargs):
        # TODO CHECK AVAILABLE CHANGE CURRENCY
        creation = False
        if not self.pk:
            creation = True


        super(AbstractTransaction, self).save(*args, **kwargs) # Call the "real" save() method

        if creation and type(self) is not Change and not self.is_change_complete():
            list_change = Change.objects.filter(new_currency=self.currency, date__lte=self.date, balance__gt=0).order_by('date')
            for c in list_change:
                if self.due_to_change() is not 0:
                    if c.balance >= self.due_to_change():
                        Transaction2Change.objects.create(transaction=self,
                                                          transaction_amount=self.due_to_change(),
                                                          change=c,
                                                          change_amount=(c.amount*self.due_to_change()/c.new_amount))
                    else:
                        Transaction2Change.objects.create(transaction=self,
                                                          transaction_amount=c.balance,
                                                          change=c,
                                                          change_amount=(c.amount*c.balance/c.new_amount))



    def value(self):
        return self.currency.verbose(self.amount)

    def is_change_complete(self):
        if self.account.currency is self.currency:
            return True

        if self.t2c.aggregate(Sum('transaction_amount'))['transaction_amount__sum'] == self.amount:
            return True

        return False

    def due_to_change(self):
        due = self.t2c.aggregate(Sum('transaction_amount'))['transaction_amount__sum']
        if due is None:
            return self.amount
        return self.amount - due

    def reference_value(self):
        if self.currency is not self.account.currency:
            if self.is_change_complete():
                return self.t2c.aggregate(Sum('change_amount'))['change_amount__sum']
            else:
                return None
        return self.amount

    def delete(self, *args, **kwargs):
        change = None

        if self.currency is not self.account.currency and len(self.t2c.all()) > 0:
            change = Change.objects.filter(transactions__in=self.t2c.all()).order_by('date')[0]
            for t in self.t2c.all():
                t.delete()

        super(AbstractTransaction, self).delete(*args, **kwargs) # Call the "real" delete() method

        if change is not None:
            change = Change.objects.get(pk=change.pk)
            recalculateAllTransactionsAfterChange(change)


class DebitsCredits(AbstractTransaction):

    def __unicode__(self):
        return u"%s" % (self.name,)


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
    balance      = models.FloatField(_(u'Balance'), editable=False, help_text=_(u"Ammount of cash in the new currency"))

    def __unicode__(self):
        return u"%d %s (%s -> %s) : %f" % (self.pk, self.name, self.currency.verbose(self.amount), self.new_currency.verbose(self.new_amount), self.balance)

    def force_save(self, *args, **kwargs):
        super(Change, self).save(*args, **kwargs) # Call the "real" save() method

    def save(self, *args, **kwargs):

        # IF CHANGE DATE MOVE, REMOVE ALL TRANSACTION2CHANGE ET RECALULCATE.
        # CHECK FOR PREVIOUS CHANGE IF CURRENCY IS NOT ACCOUNT CURRENCY
        # TODO CHECK UNCHANGED TRANSACTION

        if not self.pk:
            self.balance = self.new_amount
            super(Change, self).save(*args, **kwargs) # Call the "real" save() method
            recalculateAllTransactionsAfterChange(self)
        else:
            oldInstance = Change.objects.get(pk=self.pk)

            super(Change, self).save(*args, **kwargs) # Call the "real" save() method

            # if oldInstance is older, mean Change have been moved up.
            if oldInstance.date == self.date:
                recalculateAllTransactionsAfterChange(self)
            else:
                try:
                    firstChange = Change.objects.filter(account=self.account, date__lte=oldInstance.date).order_by('-date')[0]
                    recalculateAllTransactionsAfterChange(firstChange)
                except:
                    recalculateAllTransactionsAfterChange(self)



    def exchange_rate(self):
        return self.new_amount / self.amount

class Transaction2Change(models.Model):
    """
        When doing transaction in foreign currency, will check if change have been done before
        and estimate precisely price in default currency.
        This allow to link a transaction and a change.
    """
    transaction         = models.ForeignKey(AbstractTransaction, related_name='t2c')
    transaction_amount  = models.FloatField(_(u'Transaction Amount'), null=False, blank=False, help_text=_(u"Part of the old transaction from this change."))
    change              = models.ForeignKey(Change, related_name='transactions')
    change_amount       = models.FloatField(_(u'Change Amount'), null=False, blank=False, help_text=_(u"Value in the new Currency."))

    def __unicode__(self):
        return u"%d %s %s" % (self.pk, self.transaction, self.change)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.change.balance -= self.transaction_amount
            self.change.force_save()
        super(Transaction2Change, self).save(*args, **kwargs) # Call the "real" save() method

    def delete(self, *args, **kwargs):
        self.change.balance += self.transaction_amount
        self.change.force_save()
        super(Transaction2Change, self).delete(*args, **kwargs) # Call the "real" delete() method

