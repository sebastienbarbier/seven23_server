"""
    Profile administration
"""
from django.contrib import admin
from seven23.models.tokens.models import DiscountCode, EmailVerificationToken
from seven23.models.tokens.models import AllowAccountAccessToken

admin.site.register(DiscountCode)
admin.site.register(EmailVerificationToken)
admin.site.register(AllowAccountAccessToken)
