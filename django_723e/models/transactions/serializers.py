
from django_723e.models.transactions.models import Category, DebitsCredits, Change
from django_723e.models.accounts.models import Account
from django_723e.models.currency.models import Currency
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class DebitsCreditsSerializer(serializers.HyperlinkedModelSerializer):
    account          = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    category         = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    local_currency   = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())
    foreign_currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    class Meta:
        model  = DebitsCredits
        fields = ('id', 'account', 'name', 'local_amount', 'local_currency', 'foreign_amount', 'foreign_currency', 'date', 'active', 'category', 'isForeignCurrency')


class ChangeSerializer(serializers.HyperlinkedModelSerializer):
    account        = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    local_currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())
    new_currency   = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    class Meta:
        model  = Change
        fields = ('id', 'account', 'name', 'local_amount', 'local_currency', 'date', 'active', 'category', 'new_amount', 'new_currency', 'exchange_rate', 'value', 'new_value')
