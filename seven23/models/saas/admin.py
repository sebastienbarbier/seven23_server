"""
    Terms and Conditions administration
"""
from django.contrib import admin
from seven23.models.saas.models import StripeCustomer, Price

admin.site.register(StripeCustomer)
admin.site.register(Price)