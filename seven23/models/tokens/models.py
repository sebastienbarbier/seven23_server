"""
    Profile models
"""
import uuid
from django.db import models
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from seven23.models.accounts.models import Account, PERMISSIONS

class AbstractToken(models.Model):
    """
        Abstract Token object.
    """
    token = models.CharField(_(u'Token'), default=uuid.uuid4, max_length=32, unique=True, editable=False)
    creationDate = models.DateField(_(u''), auto_now_add=True)

    class Meta:
        ordering = ('creationDate', 'token')

    def __str__(self):
        return u'%s' % (self.token)

class EmailVerificationToken(AbstractToken):
    """
        Token send by email to verify it
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    newEmail = models.EmailField(_(u'New email'), blank=False, null=False)

    def __str__(self):
        return u'%s' % (self.token)