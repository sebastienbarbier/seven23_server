"""
    Adminitration to accounts module
"""
from django.contrib import admin
from django_723e.models.accounts.models import Account, AccountGuests

class AccountAdmin(admin.ModelAdmin):
    """
        Admin object
    """
    list_display = ('owner', 'name', 'currency', 'create', 'archived')

class AccountGuestsAdmin(admin.ModelAdmin):
    """
        Admin object
    """
    list_display = ('account', 'user', 'permissions')

admin.site.register(Account, AccountAdmin)
admin.site.register(AccountGuests, AccountGuestsAdmin)
