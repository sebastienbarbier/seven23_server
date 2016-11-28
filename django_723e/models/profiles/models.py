"""
    Profile models
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Profile(models.Model):
    """
        An account is considere as a bank account. Name is just a label for the user interface.
    """
    user = models.OneToOneField(User)
    email_verified = models.BooleanField(_(u'Email is verified'), default=False)

    class Meta:
        ordering = ('user.username')
        verbose_name = _(u'Profile')

    def __unicode__(self):
        return u'%s' % (self.user.username)
