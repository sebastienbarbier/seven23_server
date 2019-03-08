"""
    Serialized for transactions module
"""
from rest_framework import serializers
from collections import OrderedDict
from seven23.models.accounts.models import Account
from seven23.models.currency.models import Currency
from seven23.models.categories.models import Category
from seven23.models.transactions.models import DebitsCredits, Change

from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)

class DebitsCreditsSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
        Serialized for DebitsCredits model
    """
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)

    def to_representation(self, instance):
        result = super(DebitsCreditsSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

    class Meta:
        model = DebitsCredits
        list_serializer_class = BulkListSerializer
        fields = ('id', 'account', 'category', 'blob', 'active', 'last_edited', 'deleted')


class ChangeSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
        Serializer for Change model
    """
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

    class Meta:
        model = Change
        list_serializer_class = BulkListSerializer
        fields = ('id', 'account', 'blob', 'active', 'last_edited', 'deleted')