"""
    Serializer for Categories module
"""
from rest_framework import serializers
from seven23.models.accounts.models import Account
from seven23.models.categories.models import Category

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Category model
    """
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)

    class Meta:
        model = Category
        fields = ('id', 'account', 'blob', 'active', 'last_edited', 'deleted')
