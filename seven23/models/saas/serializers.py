"""
    Serializer for Currency module
"""
from rest_framework import serializers
from seven23.models.saas.models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    class Meta:
        model = Product
        fields = ('pk', 'price', 'currency', 'duration', 'is_active')