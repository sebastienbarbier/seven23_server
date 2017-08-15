"""
    Serialized for transactions module
"""
from rest_framework import serializers
from seven23.models.accounts.models import Account
from seven23.models.currency.models import Currency
from seven23.models.categories.models import Category
from seven23.models.transactions.models import DebitsCredits, Change, PaidBy
from seven23.models.events.models import Attendee
from seven23.models.events.serializers import AttendeeSerializer

class PaidBySerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialized for DebitsCredits model
    """
    transaction = serializers.PrimaryKeyRelatedField(queryset=DebitsCredits.objects.all())
    attendee = serializers.PrimaryKeyRelatedField(queryset=Attendee.objects.all())

    class Meta:
        model = PaidBy
        fields = ('id', 'transaction', 'attendee', 'amount')

class DebitsCreditsSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialized for DebitsCredits model
    """
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    local_currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    payments = PaidBySerializer(many=True)

    class Meta:
        model = DebitsCredits
        fields = ('id', 'account', 'name', 'local_amount', 'local_currency', 'date', 'active',
                  'category', 'last_edited', 'payments')


class ChangeSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serializer for Change model
    """
    queryset = Currency.objects.all()

    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    local_currency = serializers.PrimaryKeyRelatedField(queryset=queryset)
    new_currency = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = Change
        fields = ('id', 'account', 'name', 'local_amount', 'local_currency', 'date', 'active',
                  'category', 'new_amount', 'new_currency', 'exchange_rate', 'last_edited')
