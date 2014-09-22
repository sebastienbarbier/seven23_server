
from django_723e.models.transactions.models import Category, DebitsCredits, Cheque, Change, Tranfert
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'user', 'name', 'description', 'color', 'icon', 'parent', 'selectable', 'active')

class DebitsCreditsSerializer(serializers.HyperlinkedModelSerializer):
    is_complete = serializers.Field(source='is_change_complete')
    reference_value = serializers.Field(source='reference_value')

    class Meta:
        model = DebitsCredits
        fields = ('id', 'account', 'currency', 'name', 'amount', 'date', 'active', 'category', 'is_complete', 'reference_value')


class ChequeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cheque
        fields = ('id', 'account', 'currency', 'name', 'amount', 'date', 'active', 'category', 'cheque_name', 'place', 'debit_date')

class ChangeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Change
        fields = ('id', 'account', 'currency', 'name', 'amount', 'date', 'active', 'category', 'new_amount', 'new_currency', 'balance')

class TranfertSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tranfert
        fields = ('id', 'account', 'currency', 'name', 'amount', 'date', 'active', 'category', 'account_dest')

