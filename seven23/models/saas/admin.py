"""
    Terms and Conditions administration
"""
from django.contrib import admin
from seven23.models.saas.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('duration', 'price', 'currency')

admin.site.register(Product, ProductAdmin)