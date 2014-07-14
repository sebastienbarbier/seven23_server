# -*- coding: utf-8 -*-

from django.contrib import admin
from django_723e.models.transactions.models import Category, Transaction, Change, Tranfert, Cheque

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user','name','parent','active')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'date', 'amount', 'currency', 'category', 'active', 'reference_value')
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

admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Tranfert, TranfertAdmin)
admin.site.register(Cheque, ChequeAdmin)