"""
    Terms and Conditions administration
"""
from django.contrib import admin
from seven23.models.terms.models import TermsAndConditions

admin.site.register(TermsAndConditions)
