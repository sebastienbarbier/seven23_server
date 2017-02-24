"""
    Profile administration
"""
from django.contrib import admin
from django_723e.models.tokens.models import DiscountCode, EmailVerificationToken
from django_723e.models.tokens.models import AllowAccountAccessToken

admin.site.register(DiscountCode)
admin.site.register(EmailVerificationToken)
admin.site.register(AllowAccountAccessToken)
