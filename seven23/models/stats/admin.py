"""
    Terms and Conditions administration
"""
from django.contrib import admin
from seven23.models.stats.models import MonthlyActiveUser, DailyActiveUser

class MonthlyActiveUserAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'counter')

class DailyActiveUserAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'day', 'counter')

admin.site.register(MonthlyActiveUser, MonthlyActiveUserAdmin)
admin.site.register(DailyActiveUser, DailyActiveUserAdmin)