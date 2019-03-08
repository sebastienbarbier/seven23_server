"""
    Admin transactions module
"""
from django.contrib import admin
from seven23.models.transactions.models import DebitsCredits, Change

class DebitsCreditsAdmin(admin.ModelAdmin):
    """ DebitsCredits model """
    list_display = ('account', 'category', 'last_edited', 'active')
    list_filter = ('account', 'active')

class ChangeAdmin(admin.ModelAdmin):
    """ Change model """
    list_display = ('account', 'last_edited', 'active')
    list_filter = ('account', 'active')

admin.site.register(DebitsCredits, DebitsCreditsAdmin)
admin.site.register(Change, ChangeAdmin)