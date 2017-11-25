"""
    Currency models
"""
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

class Currency(models.Model):
    """
        Use to specify an ammount's currency with this object.
    """
    CHOICES = ((False, _(u'Before the amount')), (True, _(u'After the amount')))

    name = models.CharField(_('Name'), max_length=128)
    sign = models.CharField(_('Sign'), max_length=6)
    space = models.BooleanField(_(u'Add a space between amount and sign'), default=True)
    after_amount = models.BooleanField(_(u'Sign position'), choices=CHOICES, default=True)
    favorite = models.ManyToManyField(User, related_name="favoritesCurrencies")

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Currency')

    def __str__(self):
        return u'%s (%s)' % (self.name, self.sign)

    def verbose(self, amount):
        """
            Return buildel value
        """
        res = ""
        if not self.after_amount:
            res += self.sign
            if self.space:
                res += " "
            res += "%0.2f" % amount
        else:
            res += "%0.2f" % amount
            if self.space:
                res += " "
            res += self.sign
        return res


