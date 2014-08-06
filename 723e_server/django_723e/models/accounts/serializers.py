from django_723e.models.accounts.models import Account
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class AccountSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'user', 'name', 'create', 'currency', 'archived')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')
