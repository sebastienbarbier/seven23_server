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
    name = models.CharField(_(u'Name'), max_length=128)
    description = models.TextField(_(u'Description'), blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    selectable = models.BooleanField(_(u'Selectable'),
                                     default=True,
                                     help_text=_(u"Can be link to a transaction"))
    active = models.BooleanField(_(u'Enable'),
                                 default=True,
                                 help_text=_(u"Delete a category only disable it"))

    def __str__(self):
        return u'%s' % (self.name)

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
            super(Category, self).delete()
