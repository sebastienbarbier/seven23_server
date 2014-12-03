from django_723e.models.accounts.models import Account
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class AccountSerializer(serializers.HyperlinkedModelSerializer):

    currency = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'name', 'create', 'currency', 'archived')


class UserSerializer(serializers.ModelSerializer):

    accounts = AccountSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'accounts')
