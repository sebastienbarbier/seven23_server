# -*- coding: utf-8 -*-

from django.contrib import admin
from django_723e.models.currency.models import Currency

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'sign', 'space', 'after_amount',)

admin.site.register(Currency, CurrencyAdmin)