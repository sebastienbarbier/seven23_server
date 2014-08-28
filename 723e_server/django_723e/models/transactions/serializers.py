from django_723e.models.transactions.models import Category
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'user', 'name', 'description', 'color', 'icon', 'parent', 'selectable', 'active')

