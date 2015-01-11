# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models import Sum
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
        from django_723e.models.transactions.models import AbstractTransaction


        if date1 > date2:
            date1, date2 = date2, date1

        return AbstractTransaction.objects.filter(date__gte=date1, date__lte=date2, active=True, category__exact=self).aggregate(Sum('amount'))['amount__sum']

