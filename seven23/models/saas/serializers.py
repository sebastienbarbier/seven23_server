"""
    Serializer for Currency module
"""
from rest_framework import serializers
from seven23.models.saas.models import Price, StripeSubscription

class StripeSubscriptionSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """

    class Meta:
        model = StripeSubscription
        fields = ('pk', 'subscription_id', 'current_period_end', 'is_active', 'is_trial', 'is_canceled')

class PriceSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    class Meta:
        model = Price
        fields = ('pk', 'stripe_price_id', 'price', 'currency', 'duration', 'enabled')