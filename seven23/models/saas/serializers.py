"""
    Serializer for Currency module
"""
from rest_framework import serializers
from seven23.models.saas.models import Price, StripeCustomer

class StripeCustomerSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    class Meta:
        model = StripeCustomer
        fields = ('pk', 'stripe_customer_id', 'stripe_subscription_id', 'is_active')

class PriceSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    class Meta:
        model = Price
        fields = ('pk', 'stripe_price_id', 'price', 'currency', 'duration', 'enabled')