"""
    api/va/accounts views
"""

import json
from django.contrib.auth import authenticate
# Default user model may get swapped out of the system and hence.
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, permissions
from rest_framework_bulk import BulkModelViewSet

from seven23.api.permissions import IsPaid
from seven23.models.accounts.models import Account
from seven23.models.accounts.serializers import AccountSerializer

class AccountsList(BulkModelViewSet):
    """
        Distribute Account model object
    """
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated, IsPaid)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Account.objects.none()

        return self.request.user.accounts.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def allow_bulk_destroy(self, qs, filtered):

        if isinstance(self.request.data, list):
            return True
        return False