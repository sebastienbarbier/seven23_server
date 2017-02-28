"""
    Views for api/va/transactions
"""
from itertools import chain

from seven23.models.categories.models import Category
from seven23.models.categories.serializers import CategorySerializer
from seven23.models.transactions.models import DebitsCredits, Change
from seven23.models.transactions.serializers import DebitsCreditsSerializer, ChangeSerializer

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
        return obj.account.id in list(chain(
            request.user.accounts.values_list('id', flat=True),
            request.user.guests.values_list('account__id', flat=True)
        ))

#
# List of entry points Category, DebitsCredits, Change
#

class ApiCategories(viewsets.ModelViewSet):
    """
        Deliver Categor model object
    """
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, CanWriteAccount)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('account',)

    def get_queryset(self):
        return Category.objects.filter(
            account__in=list(chain(
                self.request.user.accounts.values_list('id', flat=True),
                self.request.user.guests.values_list('account__id', flat=True)
            ))
        )
