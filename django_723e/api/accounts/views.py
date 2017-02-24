"""
    api/va/accounts views
"""

from django.contrib.auth import authenticate
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User

from rest_framework import viewsets, generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django_723e import settings
from django_723e.models.accounts.models import Account
from django_723e.models.accounts.serializers import AccountSerializer
from django_723e.models.currency.models import Currency

class AccountsList(viewsets.ModelViewSet,
                   generics.RetrieveUpdateDestroyAPIView):
    """
        Distribute Account model object
    """
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.accounts.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
