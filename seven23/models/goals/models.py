"""
    Goals models
"""
from django.db import models
from django.utils.translation import ugettext as _

from seven23.models.accounts.models import Account

class Goals(models.Model):
    """
        Money transaction.
    """
    account = models.ForeignKey(Account, related_name='goals', on_delete=models.CASCADE)
    blob = models.TextField(_('blob'), blank=True, null=False)
    last_edited = models.DateTimeField(_(u'Last edited'), auto_now=True)
    deleted = models.BooleanField(_(u'Deleted'),
                                 default=False,
                                 help_text=_(u"If true, this entry has been deleted "\
                                 "and we keep this is as deleted as a tombstone."))

    def __str__(self):
        return u"(%d) %s... %s" % (self.pk, self.blob[:10], self.last_edited)

    def delete(self):
        self.deleted = True
        self.blob = ''
        self.save()