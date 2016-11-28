"""
    Serialized for transactions module
"""
from rest_framework import serializers
from django_723e.models.accounts.models import Account
from django_723e.models.currency.models import Currency
from django_723e.models.transactions.models import Category, DebitsCredits, Change

class DebitsCreditsSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialized for DebitsCredits model
    """
    queryset = Currency.objects.all()

    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    local_currency = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = DebitsCredits
        fields = ('id', 'account', 'name', 'local_amount', 'local_currency', 'date', 'active',
                  'category')


class ChangeSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer for Change model
    """
    queryset = Currency.objects.all()

    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    local_currency = serializers.PrimaryKeyRelatedField(queryset=queryset)
    new_currency = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Change
        fields = ('id', 'account', 'name', 'local_amount', 'local_currency', 'date', 'active',
                  'category', 'new_amount', 'new_currency', 'exchange_rate')
