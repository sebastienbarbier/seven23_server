"""
    Adminitration to accounts module
"""
from django.contrib import admin
from django_723e.models.accounts.models import Account, InvitationRequest

class AccountAdmin(admin.ModelAdmin):
    """
        Admin object
    """
    list_display = ('user', 'name', 'currency', 'create', 'archived')

class InvitationRequestAdmin(admin.ModelAdmin):
    """
        Invitation object
    """
    list_display = ('create', 'email')

admin.site.register(Account, AccountAdmin)
admin.site.register(InvitationRequest, InvitationRequestAdmin)
