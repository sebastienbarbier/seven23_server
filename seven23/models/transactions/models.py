"""
    Transactions models
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from seven23.models.accounts.models import Account
from seven23.models.categories.models import Category
from seven23.models.currency.models import Currency
from seven23.models.events.models import Attendee, Event

class AbstractTransaction(models.Model):
    """
        Money transaction.
    """
    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)
    blob = models.TextField(_('blob'), blank=True, null=False)
    last_edited = models.DateTimeField(_(u'Last edited'), auto_now=True)
    active = models.BooleanField(_(u'Enable'),
                                 default=True,
                                 help_text=_(u"A disabled transaction will be save as a "\
                                 "draft and not use in any report."))

    def __str__(self):
        return u"(%d) %s... %s" % (self.pk, self.blob[:10], self.last_edited)

class DebitsCredits(AbstractTransaction):
    """
        Simpliest transaction model
    """

    class Meta:
        verbose_name = _(u'DebitsCredit')
        verbose_name_plural = _(u'DebitsCredits')

class Change(AbstractTransaction):
    """
        Change money in a new currency.
    """

    class Meta:
        verbose_name = _(u'Change')
        verbose_name_plural = _(u'Changes')
