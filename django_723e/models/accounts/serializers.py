from django_723e.models.accounts.models import Account, InvitationRequest
from django_723e.models.currency.models import Currency
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class AccountSerializer(serializers.HyperlinkedModelSerializer):

    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    class Meta:
        model = Account
        fields = ('id', 'name', 'create', 'currency', 'archived')


class InvitationRequestSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = InvitationRequest
        fields = ('id', 'create', 'email')


class UserSerializer(serializers.ModelSerializer):

    accounts = AccountSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'accounts')
