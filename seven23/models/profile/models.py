"""
    Terms and Conditions models
"""
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
# from seven23.models.stats.models import MonthlyActiveUser, DailyActiveUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from django.conf import settings

class Profile(models.Model):
    """
        Discount token on puschase in SAS mode.
    """
    AVATAR_OPTIONS = (
        ('NONE', 'None'),
        ('GRAVATAR', 'Gravatar'),
        ('NOMADLIST', 'Nomadlist'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(_(u'Avatar'),
                                default='NONE',
                                max_length=20,
                                choices=AVATAR_OPTIONS,
                                help_text=_(u'Select between different origins.'))
    social_networks = models.TextField(_('social_networks blob'), blank=True, null=False)
    last_api_call = models.DateField(_(u'Last API call'),
                                help_text=_(u'Last call on the API as a registered user'),
                                auto_now_add=True,
                                editable=False)
    valid_until = models.DateTimeField(_(u'Valid until'),
                                help_text=_(u'On SASS, this is the validation date'),
                                default=timezone.now)
    stripe_customer_id = models.CharField(_(u'Stripe costumer id'),
                                max_length=128,
                                null=True,
                                blank=True,
                                help_text=_(u'Generated by Stripe\'s API'))

    def save(self, *args, **kwargs):
        if self.pk is None:
            if not self.user.email.endswith('seven23.io'):
                send_mail(
                    '[seven23.io] New user',
                    render_to_string('registration/new_user.txt', {"user": self.user}),
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False
                )

            self.valid_until = timezone.now() + datetime.timedelta(days=settings.TRIAL_PERIOD)

        super(Profile, self).save(*args, **kwargs) # Call the "real" save() method

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            Profile.objects.create(user=instance)

    def __str__(self):
        return u'%s' % (self.user)

@receiver(pre_delete, sender=Profile)
def on_delete_profile(sender, instance, **kwargs):
    if not instance.user.email.endswith('seven23.io'):
        send_mail(
            '[seven23.io] Deleted user',
            render_to_string('registration/delete_user.txt', {"user": instance.user}),
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=False
        )