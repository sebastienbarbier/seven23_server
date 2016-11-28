"""
    Serializer for accounts module
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from django_723e.models.accounts.models import Account, InvitationRequest
from django_723e.models.currency.models import Currency

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    """
        Account serializer
    """
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    class Meta:
        model = Account
        fields = ('id', 'name', 'create', 'currency', 'archived')


class InvitationRequestSerializer(serializers.HyperlinkedModelSerializer):
    """
        Invitation serializer
    """
    class Meta:
        model = InvitationRequest
        fields = ('id', 'create', 'email')


class UserSerializer(serializers.ModelSerializer):
    """
        User serializer
    """
    accounts = AccountSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'accounts')
