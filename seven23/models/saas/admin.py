"""
    Terms and Conditions administration
"""
from django.contrib import admin
from seven23.models.saas.models import StripeSubscription, Price

admin.site.register(StripeSubscription)
admin.site.register(Price)