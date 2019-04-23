"""
    Terms and Conditions administration
"""
from django.contrib import admin
from seven23.models.saas.models import Charge, Product, Coupon

class ChargeAdmin(admin.ModelAdmin):
    search_fields = ['reference_id']
    list_display = ('user', 'status', 'date', 'paiment_method', 'apply_coupon', 'coupon')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('duration', 'price', 'currency')

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'percent_off', 'is_active')


admin.site.register(Charge, ChargeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Coupon, CouponAdmin)