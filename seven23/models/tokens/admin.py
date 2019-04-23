"""
    Profile administration
"""
from django.contrib import admin
from seven23.models.tokens.models import EmailVerificationToken

admin.site.register(EmailVerificationToken)