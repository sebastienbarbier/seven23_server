"""
    Terms and Conditions models
"""
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from seven23.models.stats.models import MonthlyActiveUser, DailyActiveUser

from django.conf import settings

class Profile(models.Model):
    """
        Discount token on puschase in SAS mode.
    """
    AVATAR_OPTIONS = (
        ('NONE', 'None'),
        ('GRAVATAR', 'Gravatar'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(_(u'Avatar'),
                                default='NONE',
                                max_length=20,
                                choices=AVATAR_OPTIONS,
                                help_text=_(u'Select between different origins.'))
    last_api_call = models.DateField(_(u'Last API call'),
                                help_text=_(u'Last call on the API as a registered user'),
                                auto_now_add=True,
                                editable=False)
    valid_until = models.DateTimeField(_(u'Valid until'),
                                help_text=_(u'On SASS, this is the validation date'),
                                default=datetime.datetime.now() + datetime.timedelta(days=settings.TRIAL_PERIOD))

    def save(self, *args, **kwargs):
        if self.pk is None:

            send_mail(
                '[seven23.io] New user',
                render_to_string('registration/new_user.txt', {"user": self.user}),
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False
            )

            now = datetime.datetime.now()
            # Add it as active user
            monthlyActiveUser = MonthlyActiveUser.objects.get_or_create(year=now.year, month=now.month)[0]
            monthlyActiveUser.counter += 1
            monthlyActiveUser.save()

            dailyActiveUser = DailyActiveUser.objects.get_or_create(year=now.year, month=now.month, day=now.day)[0]
            dailyActiveUser.counter += 1
            dailyActiveUser.save()

        super(Profile, self).save(*args, **kwargs) # Call the "real" save() method

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return u'%s' % (self.user)