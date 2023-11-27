"""
    Terms and Conditions administration
"""
from django.contrib import admin
from seven23.models.saas.models import Charge, Product

class ChargeAdmin(admin.ModelAdmin):
    search_fields = ['reference_id']
    list_display = ('user', 'status', 'date', 'paiment_method')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('duration', 'price', 'currency')

admin.site.register(Charge, ChargeAdmin)
admin.site.register(Product, ProductAdmin)