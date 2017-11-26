"""
    Serializer for Currency module
"""
from seven23.models.currency.models import Currency
from rest_framework import serializers

class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    class Meta:
        model = Currency
        fields = ('id', 'name', 'code','sign', 'space', 'after_amount')
