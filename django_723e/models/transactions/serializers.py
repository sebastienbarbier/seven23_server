
from django_723e.models.transactions.models import Category, DebitsCredits, Change
from django_723e.models.accounts.models import Account
from django_723e.models.currency.models import Currency
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class DebitsCreditsSerializer(serializers.HyperlinkedModelSerializer):

    queryset = Currency.objects.all()

    account          = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    category         = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    local_currency   = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model  = DebitsCredits
        fields = ('id', 'account', 'name', 'local_amount', 'local_currency', 'date', 'active', 'category')


class ChangeSerializer(serializers.HyperlinkedModelSerializer):

    queryset = Currency.objects.all()

    account        = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    local_currency = serializers.PrimaryKeyRelatedField(queryset=queryset)
    new_currency   = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model  = Change
        fields = ('id', 'account', 'name', 'local_amount', 'local_currency', 'date', 'active', 'category', 'new_amount', 'new_currency', 'exchange_rate')
