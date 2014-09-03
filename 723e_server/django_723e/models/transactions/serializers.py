from django_723e.models.transactions.models import Category, Transaction
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'user', 'name', 'description', 'color', 'icon', 'parent', 'selectable', 'active')



class TransactionSerializer(serializers.HyperlinkedModelSerializer):

    is_complete = serializers.Field(source='is_change_complete')
    reference_value = serializers.Field(source='reference_value')

    class Meta:
        model = Transaction
        fields = ('id', 'account', 'currency', 'name', 'amount', 'date', 'active', 'category', 'is_complete', 'reference_value')
