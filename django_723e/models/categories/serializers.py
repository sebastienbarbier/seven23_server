"""
    Serializer for Categories module
"""
from rest_framework import serializers
from django_723e.models.accounts.models import Account
from django_723e.models.categories.models import Category

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Category model
    """
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        fields = ('id', 'account', 'name', 'description', 'parent', 'selectable', 'active')
