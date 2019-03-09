"""
    Terms and Conditions models
"""
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class MonthlyActiveUser(models.Model):
    """
        Discount token on puschase in SAS mode.
    """
    year = models.IntegerField(_(u'Year'), default=datetime.now().year, editable=False)
    month = models.IntegerField(_(u'Month'), default=datetime.now().month, editable=False)
    counter = models.IntegerField(_(u'Counter'), default=0, editable=False)

    class Meta:
        ordering = ('year', 'month')

    def __str__(self):
        return u'%i-%i' % (self.year, self.month)

class DailyActiveUser(models.Model):
    """
        Discount token on puschase in SAS mode.
    """
    year = models.IntegerField(_(u'Year'), default=datetime.now().year, editable=False)
    month = models.IntegerField(_(u'Month'), default=datetime.now().month, editable=False)
    day = models.IntegerField(_(u'Day'), default=datetime.now().day, editable=False)
    counter = models.IntegerField(_(u'Counter'), default=0, editable=False)

    class Meta:
        ordering = ('year', 'month', 'day')

    def __str__(self):
        return u'%i-%i-%i' % (self.year, self.month, self.day)