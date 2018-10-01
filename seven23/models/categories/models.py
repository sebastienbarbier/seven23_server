# -*- coding: utf-8 -*-
"""
    Models for categories module
"""
from django.db import models
from django.utils.translation import ugettext as _

from seven23.models.accounts.models import Account

class Category(models.Model):
    """
        Category of transaction.
    """
    account = models.ForeignKey(Account, related_name='categories', blank=True, null=True, on_delete=models.CASCADE)
    blob = models.TextField(_('blob'), blank=True, null=False)
    active = models.BooleanField(_(u'Enable'),
                                 default=True,
                                 help_text=_(u"Delete a category only disable it"))
    last_edited = models.DateTimeField(_(u'Last edited'), auto_now=True)
    deleted = models.BooleanField(_(u'Deleted'),
                                 default=False,
                                 help_text=_(u"If true, this entry has been deleted "\
                                 "and we keep this is as deleted as a tombstone."))

    def __str__(self):
        return u'(%d) %s...' % (self.pk, self.blob[:10])

    def enable(self):
        """ Enable """
        self.active = True
        self.save()

    def disable(self):
        """ Disable """
        self.active = False
        self.save()

    def toggle(self):
        """ Toggle """
        if self.active:
            self.disable()
        else:
            self.enable()

    def delete(self):
        """
            If a category object is link to a transaction, it cannot be delete because
            we need to keep trace of all transactions. It is only disable/hide.
        """
        if self.transactions.all():
            self.toggle()
        else:
            self.deleted = True
            self.blob = ''
            self.save()
