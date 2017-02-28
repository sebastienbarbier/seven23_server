"""
    Adminitration to accounts module
"""
from django.contrib import admin
from seven23.models.accounts.models import Account, AccountGuests

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
