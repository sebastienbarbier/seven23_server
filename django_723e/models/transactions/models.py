"""
    Transactions models
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django_723e.models.accounts.models import Account
from django_723e.models.categories.models import Category
from django_723e.models.currency.models import Currency

class AbstractTransaction(models.Model):
    """
        Money transaction.
    """
    account = models.ForeignKey(Account, related_name='transactions')
    name = models.CharField(_(u'Name'), max_length=255)
    local_amount = models.FloatField(_(u'Amount'),
                                     null=False,
                                     blank=False,
                                     help_text=_(u"Credit and debit are represented by "\
                                     "positive and negative value."))
    local_currency = models.ForeignKey(Currency, related_name='transactions')
    date = models.DateField(_(u'Date'), editable=True, default=timezone.now)
    active = models.BooleanField(_(u'Enable'),
                                 default=True,
                                 help_text=_(u"A disabled transaction will be save as a "\
                                 "draft and not use in any report."))
    category = models.ForeignKey(Category, related_name='transactions', blank=True, null=True)
    last_edited = models.DateTimeField(_(u'Last edited'), auto_now=True)

    def __unicode__(self):
        return u"(%d) %s %s" % (self.pk, self.name, self.local_currency.verbose(self.local_amount))

    def update_amount(self, *args, **kwargs):
        """ Update amount. Deprecated """
        pass

    def save(self, *args, **kwargs):
        self.update_amount(*args, **kwargs)
        super(AbstractTransaction, self).save(*args, **kwargs) # Call the "real" save() method

    def value(self):
        """ Return a stringify currency base value """
        return self.local_currency.verbose(self.local_amount)

class DebitsCredits(AbstractTransaction):
    """
        Simpliest transaction model
    """
    def save(self, *args, **kwargs):
        super(DebitsCredits, self).save(*args, **kwargs) # Call the "real" save() method

    class Meta:
        verbose_name = _(u'DebitsCredit')
        verbose_name_plural = _(u'DebitsCredits')

    def __unicode__(self):
        return u"%s" % (self.name)

class Change(AbstractTransaction):
    """
        Change money in a new currency.
    """
    new_amount = models.FloatField(_(u'New Amount'),
                                   null=False,
                                   blank=False,
                                   help_text=_(u"Amount of cash in the new currency"))
    new_currency = models.ForeignKey(Currency, related_name="change", blank=True, null=True)

    def __unicode__(self):
        return u"%d %s (%s -> %s)" % (self.pk,
                                      self.name,
                                      self.local_currency.verbose(self.amount),
                                      self.new_currency.verbose(self.new_amount))

    class Meta:
        verbose_name = _(u'Change')
        verbose_name_plural = _(u'Changes')

    def force_save(self, *args, **kwargs):
        """ Force saving """
        super(Change, self).save(*args, **kwargs) # Call the "real" save() method

    def save(self, *args, **kwargs):
        # First save to have correct value
        super(Change, self).save(*args, **kwargs) # Call the "real" save() method

    def delete(self, *args, **kwargs):
        super(Change, self).delete(*args, **kwargs) # Call the "real" save() method

    def exchange_rate(self):
        """ Return exchange rate """
        return float(self.new_amount) / float(self.local_amount)

    def new_value(self):
        """ New value stringified """
        return self.new_currency.verbose(self.new_amount)
