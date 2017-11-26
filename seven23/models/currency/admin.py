# -*- coding: utf-8 -*-
"""
    Currency administration
"""
from django.contrib import admin
from seven23.models.currency.models import Currency

class CurrencyAdmin(admin.ModelAdmin):
    """
        Administrate Currency model
    """
    list_display = ('name', 'code', 'sign', 'space', 'after_amount',)

admin.site.register(Currency, CurrencyAdmin)