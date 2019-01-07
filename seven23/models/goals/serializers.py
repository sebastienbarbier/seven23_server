"""
    Serialized for transactions module
"""
from rest_framework import serializers
from seven23.models.accounts.models import Account
from seven23.models.goals.models import Goals

from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)

class GoalsSerializer(BulkSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
        Serialized for DebitsCredits model
    """
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

    class Meta:
        model = Goals
        list_serializer_class = BulkListSerializer
        fields = ('id', 'account', 'blob', 'last_edited')