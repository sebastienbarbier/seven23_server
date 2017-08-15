"""
    Views for api/va/transactions
"""
from itertools import chain

from seven23.models.events.models import Attendee
from seven23.models.events.serializers import AttendeeSerializer

from rest_framework import viewsets, permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status

import django_filters
from django_filters.rest_framework import DjangoFilterBackend

class CanWriteAttendee(permissions.BasePermission):
    """
        Object-level permission to only allow owners of an object to edit it.
        Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        # Instance must have an attribute named `owner`.
        return obj.event.account.id in list(chain(
            request.user.accounts.values_list('id', flat=True),
            request.user.guests.values_list('account__id', flat=True)
        ))

class AttendeeFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Attendee
        fields = ['event']

#
# List of entry points Category, DebitsCredits, Change
#
class ApiAttendee(viewsets.ModelViewSet):
    """
        Deliver Change objects
    """
    serializer_class = AttendeeSerializer
    permission_classes = (permissions.IsAuthenticated, CanWriteAttendee)
    filter_backends = (DjangoFilterBackend,)
    filter_class = AttendeeFilter

    def get_queryset(self):
        return Attendee.objects.filter(
            event__account__in=list(chain(
                self.request.user.accounts.values_list('id', flat=True),
                self.request.user.guests.values_list('account__id', flat=True)
            ))
        )
