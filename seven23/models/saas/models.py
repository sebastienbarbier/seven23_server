"""
    Terms and Conditions models
"""
import datetime
import calendar
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return timezone.make_aware(datetime.datetime(year, month, day, sourcedate.hour, sourcedate.minute, sourcedate.second))

class Product(models.Model):
    price = models.FloatField(_(u'Price'))
    currency = models.CharField(_(u'Currency'), max_length=3, default='EUR')
    duration = models.IntegerField(_(u'How many month to add'), help_text=_(u'Per month'), default=12)
    valid_until = models.DateField(_(u'Valid until'), null=True, blank=True)
    enabled = models.BooleanField(_(u'Enabled'), default=True)
    stripe_product_id = models.CharField(_(u'Stripe product id'), max_length=128, help_text=_(u'Looks like prod_HKHuxHWnp5SnIL'))

    def is_active(self):
        return self.enabled and (not self.valid_until or self.valid_until < datetime.datetime.now())

    def __str__(self):
        return u'%s %s' % (self.price, self.currency)

    def delete(self, *args, **kwargs):
        """
            If a category object is link to a transaction, it cannot be delete because
            we need to keep trace of all transactions. It is only disable/hide.
        """
        if self.charges.all():
            self.enabled = False
            self.save()
        else:
            super(Product, self).delete(*args, **kwargs) # Call the "real" save() method