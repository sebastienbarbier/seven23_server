"""
    Admin code for categories module
"""

from django.contrib import admin
from seven23.models.categories.models import Category

class CategoryAdmin(admin.ModelAdmin):
    """
        Deliver category model
    """
    list_display = ('account', 'active')

admin.site.register(Category, CategoryAdmin)
