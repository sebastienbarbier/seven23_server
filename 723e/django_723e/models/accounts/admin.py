# -*- coding: utf-8 -*-

from django.contrib import admin
from django_723e.models.accounts.models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'currency', 'create', 'archived')

admin.site.register(Account, AccountAdmin)