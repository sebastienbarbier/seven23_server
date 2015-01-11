# -*- coding: utf-8 -*-

from django.contrib import admin
from django_723e.models.transactions.models import DebitsCredits, Change, Tranfert, Cheque

class DebitsCreditsAdmin(admin.ModelAdmin):
    list_display = ('account', 'date', 'amount', 'currency', 'category', 'active')
    list_filter = ('account', 'currency')

class ChangeAdmin(admin.ModelAdmin):
    list_display = ('account', 'date', 'amount', 'currency', 'new_amount', 'new_currency', 'category', 'active', 'exchange_rate')
    list_filter = ('account', 'currency')

class TranfertAdmin(admin.ModelAdmin):
    list_display = ('account', 'date', 'amount', 'currency', 'category', 'active')
    list_filter = ('account', 'currency')

class ChequeAdmin(admin.ModelAdmin):
    list_display = ('account', 'date', 'amount', 'currency', 'category', 'active')
    list_filter = ('account', 'currency')

admin.site.register(DebitsCredits, DebitsCreditsAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Tranfert, TranfertAdmin)
admin.site.register(Cheque, ChequeAdmin)
