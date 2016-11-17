
from django_723e.models.categories.models import Category
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    user      = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    parent    = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)

    class Meta:
        model  = Category
        fields = ('id', 'user', 'name', 'description', 'color', 'icon', 'parent', 'selectable', 'active')
