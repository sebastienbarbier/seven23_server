"""
    Serializer for Currency module
"""
from rest_framework import serializers
from seven23.models.saas.models import Charge, Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    class Meta:
        model = Product
        fields = ('pk', 'price', 'currency', 'duration', 'is_active')

class ChargeSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    apply_coupon = serializers.SerializerMethodField()
    product = ProductSerializer()

    def get_apply_coupon(self, obj):
        return obj.apply_coupon()

    class Meta:
        model = Charge
        fields = ('pk', 'product', 'date', 'paiment_method', 'reference_id', 'status', 'comment')