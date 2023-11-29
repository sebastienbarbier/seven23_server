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

class Price(models.Model):
    stripe_price_id = models.CharField(_(u'Stripe price id'), unique=True, max_length=128, help_text=_(u'Looks like price_*'))
    price = models.FloatField(_(u'Price'))
    currency = models.CharField(_(u'Currency'), max_length=3, default='EUR')
    duration = models.IntegerField(_(u'How many month to add'), help_text=_(u'Per month'), default=12)
    enabled = models.BooleanField(_(u'Enabled'), default=True)

    def __str__(self):
        return u'%s %s %s / %s months' % (self.stripe_price_id, self.price, self.currency, self.duration)

class StripeCustomer(models.Model):
    user = models.OneToOneField(to=User, related_name="stripe", on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    price = models.ForeignKey(Price, related_name="customers", null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username