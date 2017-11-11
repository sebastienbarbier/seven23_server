"""
    Terms and Conditions models
"""
import uuid
from django.db import models
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class TermsAndConditions(models.Model):
    """
        Discount token on puschase in SAS mode.
    """
    date = models.DateField(_(u'Creation date'),
                                help_text=_(u'Date of publication'),
                                auto_now_add=True, editable=False)
    markdown = models.TextField(_(u'Terms and conditions'),
                                help_text=_(u'Formatted in Markdown'),
                                editable=True)

    def __str__(self):
        return u'%s' % (self.date)

class SignedTermsAndConditions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    terms = models.ForeignKey(TermsAndConditions, help_text=_(u'Terms agreed with user'))

    def __str__(self):
        return u'%s %s' % (self.user.username, self.terms.date)