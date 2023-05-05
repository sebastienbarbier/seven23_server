"""
    Serializer for accounts module
"""
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User
from rest_framework import serializers
from seven23.models.accounts.models import Account, AccountGuests
from seven23.models.currency.models import Currency

from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin
)

class AccountSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
        Account serializer
    """
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())
    currencies = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all(), many=True, required=False)

    class Meta:
        model = Account
        list_serializer_class = BulkListSerializer
        fields = ('id', 'name', 'create', 'currency', 'currencies', 'archived', 'public', 'preferences')

class AccountGuestsSerializer(serializers.ModelSerializer):
    """
        User serializer
    """
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    class Meta:
        model = AccountGuests
        fields = ('account', 'user', 'currency', 'permissions')