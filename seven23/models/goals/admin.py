"""
    Admin transactions module
"""
from django.contrib import admin
from seven23.models.goals.models import Goals

class GoalsAdmin(admin.ModelAdmin):
    """ DebitsCredits model """
    list_display = ('account', 'last_edited')
    list_filter = ('account',)

admin.site.register(Goals, GoalsAdmin)