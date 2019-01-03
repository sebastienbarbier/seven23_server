"""
    Serializer for Categories module
"""
from rest_framework import serializers
from seven23.models.accounts.models import Account
from seven23.models.categories.models import Category

from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)

class CategorySerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
        Serialize Category model
    """
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)

    class Meta:
        model = Category
        list_serializer_class = BulkListSerializer
        fields = ('id', 'account', 'blob', 'active', 'last_edited', 'deleted')