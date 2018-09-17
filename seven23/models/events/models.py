"""
    Event models
"""
from django.db import models
from django.utils import timezone
# Default user model may get swapped out of the system and hence.
from django.utils.translation import ugettext as _

from seven23.models.accounts.models import Account
from seven23.models.tokens.models import AbstractToken

class Event(models.Model):
    """
        Token send by email to share access to an account
    """
    account = models.ForeignKey(Account, related_name='events', blank=False, null=False, on_delete=models.CASCADE)
    title = models.CharField(_(u'Name'), max_length=255)
    date_begin = models.DateField(_(u'Date'), editable=True, default=timezone.now)
    date_end = models.DateField(_(u'Date'), editable=True, default=timezone.now)
    archived = models.BooleanField(_(u'Archive'),
                                 default=False,
                                 help_text=_(u"Archived events will be displayed "\
                                 "with less priority."))
    class Meta:
        ordering = ('account', 'title', 'date_begin')
        verbose_name = _(u'Event')
        verbose_name_plural = _(u'Events')

    def __str__(self):
        return u'%s' % (self.title)

class Attendee(models.Model):
    event = models.ForeignKey(Event, related_name='attendees', blank=False, null=False, on_delete=models.CASCADE)
    fullname = models.CharField(_(u'Fullname'), max_length=255, blank=False, null=False)
    email = models.EmailField(_(u'Email'), blank=False, null=False)

    class Meta:
        ordering = ('event', 'fullname', 'email')
        verbose_name = _(u'Attendee')
        verbose_name_plural = _(u'Attendees')

    def __str__(self):
        return u'%s' % (self.fullname)

class EventToken(AbstractToken):
    """
        Token send by email to verify it
    """
    attendee = models.ForeignKey(Attendee, related_name='token', blank=False, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _(u'EventToken')
        verbose_name_plural = _(u'EventTokens')

    def __str__(self):
        return u'%s' % (self.token)
