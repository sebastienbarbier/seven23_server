
from django_723e.models.transactions.models import Category, DebitsCredits, Cheque, Change, Tranfert
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    parent_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'user', 'name', 'description', 'color', 'icon', 'parent', 'parent_id', 'selectable', 'active')

class DebitsCreditsSerializer(serializers.HyperlinkedModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = DebitsCredits
        fields = ('id', 'account', 'currency', 'name', 'amount', 'date', 'active', 'category', 'category_id')


class ChequeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cheque
        fields = ('id', 'account', 'currency', 'name', 'amount', 'date', 'active', 'category', 'cheque_name', 'place', 'debit_date')

class ChangeSerializer(serializers.HyperlinkedModelSerializer):
    value = serializers.Field(source='value')
    new_value = serializers.Field(source='new_value')
    exchange_rate = serializers.Field(source='exchange_rate')

    class Meta:
        model = Change
        fields = ('id', 'account', 'currency', 'name', 'amount', 'date', 'active', 'category', 'new_amount', 'new_currency', 'balance', 'value', 'new_value', 'exchange_rate')

class TranfertSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tranfert
        fields = ('id', 'account', 'currency', 'name', 'amount', 'date', 'active', 'category', 'account_dest')

