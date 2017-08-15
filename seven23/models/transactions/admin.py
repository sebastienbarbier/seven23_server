"""
    Admin transactions module
"""
from django.contrib import admin
from seven23.models.transactions.models import DebitsCredits, Change, PaidBy

class DebitsCreditsAdmin(admin.ModelAdmin):
    """ DebitsCredits model """
    list_display = ('account', 'date', 'local_amount', 'local_currency', 'category', 'active')
    list_filter = ('account', 'local_currency')

class ChangeAdmin(admin.ModelAdmin):
    """ Change model """
    list_display = ('account', 'date', 'local_amount', 'local_currency', 'new_amount',
                    'new_currency', 'category', 'active', 'exchange_rate')
    list_filter = ('account', 'local_currency')

admin.site.register(DebitsCredits, DebitsCreditsAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(PaidBy)
