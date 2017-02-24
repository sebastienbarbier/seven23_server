"""
    Views for api/va/transactions
"""
from itertools import chain

from django_723e.models.categories.models import Category
from django_723e.models.categories.serializers import CategorySerializer
from django_723e.models.transactions.models import DebitsCredits, Change
from django_723e.models.transactions.serializers import DebitsCreditsSerializer, ChangeSerializer

from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend


class CanWriteAccount(permissions.BasePermission):
    """
        Object-level permission to only allow owners of an object to edit it.
        Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        # Instance must have an attribute named `owner`.
        return obj.account in list(chain(
            request.user.accounts.values_list('id', flat=True),
            request.user.guests.values_list('account__id', flat=True)
        ))

class ApiDebitscredits(viewsets.ModelViewSet):
    """
        Deliver DebitsCredits model object

    """
    serializer_class = DebitsCreditsSerializer
    permission_classes = (permissions.IsAuthenticated, CanWriteAccount)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('account',)

    def get_queryset(self):
        return DebitsCredits.objects.filter(
            account__in=list(chain(
                self.request.user.accounts.values_list('id', flat=True),
                self.request.user.guests.values_list('account__id', flat=True)
            ))
        )
