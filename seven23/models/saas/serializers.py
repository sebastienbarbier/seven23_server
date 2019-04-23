"""
    Serializer for Currency module
"""
from rest_framework import serializers
from seven23.models.saas.models import Charge, Product, Coupon

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    class Meta:
        model = Product
        fields = ('pk', 'price', 'currency', 'duration', 'is_active')

class CouponSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    class Meta:
        model = Coupon
        fields = ('code', 'name', 'percent_off', 'affiliate', 'affiliate_percent', 'is_active')

class ChargeSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    coupon = serializers.PrimaryKeyRelatedField(queryset=Coupon.objects.all())
    apply_coupon = serializers.SerializerMethodField()
    product = ProductSerializer()
    coupon = CouponSerializer()

    def get_apply_coupon(self, obj):
        return obj.apply_coupon()

    class Meta:
        model = Charge
        fields = ('pk', 'product', 'coupon', 'apply_coupon', 'date', 'paiment_method', 'reference_id', 'status', 'comment')