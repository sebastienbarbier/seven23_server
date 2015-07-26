
from django_723e.models.categories.models import Category
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    parent_id = serializers.PrimaryKeyRelatedField(read_only=True)
    user      = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model  = Category
        fields = ('id', 'user', 'name', 'description', 'color', 'icon', 'parent', 'parent_id', 'selectable', 'active')
