# -*- coding: utf-8 -*-
"""
    Models for categories module
"""
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.utils.translation import ugettext as _

from seven23.models.accounts.models import Account

class Category(MPTTModel):
    """
        Category of transaction.
    """
    account = models.ForeignKey(Account, related_name='categories', blank=True, null=True)
    name = models.CharField(_(u'Name'), max_length=128)
    description = models.TextField(_(u'Description'), blank=True, null=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    selectable = models.BooleanField(_(u'Selectable'),
                                     default=True,
                                     help_text=_(u"Can be link to a transaction"))
    active = models.BooleanField(_(u'Enable'),
                                 default=True,
                                 help_text=_(u"Delete a category only disable it"))

    def __str__(self):
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
        """ Enable """
        self.active = True
        self.save()

    def disable(self):
        """ Disable """
        self.move_children_right()
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
        self.move_children_right()
        if self.transactions.all():
            self.toggle()
        else:
            super(Category, self).delete()
