"""
    Views for api/va/transactions
"""
from itertools import chain

from seven23.models.events.models import Event
from seven23.models.events.serializers import EventSerializer

from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status

import django_filters
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

class ApiEvent(viewsets.ModelViewSet):
    """
        Deliver Change objects
    """
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated, CanWriteAccount)
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        return Event.objects.filter(
            account__in=list(chain(
                self.request.user.accounts.values_list('id', flat=True),
                self.request.user.guests.values_list('account__id', flat=True)
            ))
        )
