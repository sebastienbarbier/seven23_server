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

class DiscountCode(AbstractToken):
    """
        Discount token on puschase in SAS mode.
    """
    pourcentageUser = models.IntegerField(_(u'User pourcentage'),
                                          help_text=_(u'Pourcentage of discount for buyer'),
                                          default=0)
    pourcentageAffiliate = models.IntegerField(_(u'Affiliate pourcentage'),
                                               help_text=_(u'Pourcentage credited to referee user'),
                                               default=0)
    referee = models.ForeignKey(User,
                                blank=True,
                                null=True, on_delete=models.CASCADE)
    validUntil = models.DateField(_(u'Valid Until'),
                                  help_text=_(u'Until when can this token be used'),
                                  blank=True,
                                  null=True)
    validCounter = models.IntegerField(_(u'How many use'),
                                       help_text=_(u'How many times can this token be used'),
                                       blank=True,
                                       null=True)

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

class AllowAccountAccessToken(AbstractToken):
    """
        Token send by email to share access to an account
    """
    sendBy = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, blank=False, null=False, on_delete=models.CASCADE)
    email = models.EmailField(_(u'User email'), blank=False, null=False)
    permission = models.CharField(max_length=1, choices=PERMISSIONS, null=False, blank=False)

    def __str__(self):
        return u'%s' % (self.token)
