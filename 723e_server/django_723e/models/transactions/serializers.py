
from django_723e.models.transactions.models import Category, DebitsCredits, Change
from django_723e.models.accounts.models import Account
from django_723e.models.currency.models import Currency
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class DebitsCreditsSerializer(serializers.HyperlinkedModelSerializer):
    account           = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    category_id       = serializers.PrimaryKeyRelatedField(read_only=True)
    currency_id       = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model  = DebitsCredits
        fields = ('id', 'account', 'currency', 'currency_id', 'name', 'amount', 'reference_amount', 'date', 'active', 'category', 'category_id', 'isForeignCurrency')


class ChangeSerializer(serializers.HyperlinkedModelSerializer):
    account       = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    currency      = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())
    new_currency  = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())
    class Meta:
        model  = Change
        fields = ('id', 'account', 'currency', 'name', 'amount', 'date', 'active', 'category', 'new_amount', 'new_currency', 'value', 'new_value', 'exchange_rate')
