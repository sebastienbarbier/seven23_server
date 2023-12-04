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

class StripeSubscription(models.Model):
    subscription_id = models.CharField(max_length=255)
    user = models.OneToOneField(to=User, related_name="stripe", null=True, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, related_name="customers", null=True, on_delete=models.CASCADE)
    # Dates
    trial_end = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at = models.DateTimeField(null=True, blank=True)
    # Status
    status = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return u'%s %s' % (self.user, self.subscription_id)

    def is_trial(self):
        return self.trial_end == self.current_period_end

    def is_canceled(self):
        return self.cancel_at is not None

    def save(self, *args, **kwargs):
        if self.user:
            valid_until = self.user.profile.valid_until
            if self.cancel_at:
                self.is_active = False
                self.user.profile.valid_until = self.cancel_at
            elif self.trial_end and self.trial_end > self.current_period_end:
                self.user.profile.valid_until = self.trial_end
            elif self.current_period_end:
                self.user.profile.valid_until = self.current_period_end
            self.user.profile.save()

        super(StripeSubscription, self).save(*args, **kwargs) # Call the "real" save() method