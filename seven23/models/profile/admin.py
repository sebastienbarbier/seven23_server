"""
    Terms and Conditions administration
"""
from django.contrib import admin
from seven23.models.profile.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'valid_until', 'key_verified','last_api_call')


admin.site.register(Profile, ProfileAdmin)