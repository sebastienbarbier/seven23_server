"""
    Serializer for Categories module
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from django_723e.models.categories.models import Category

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Category model
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Category
        fields = ('id', 'user', 'name', 'description', 'color', 'icon', 'parent',
                  'selectable', 'active')
