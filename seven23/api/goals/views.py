"""
    Views for api/va/transactions
"""
from itertools import chain

from seven23.models.goals.models import Goals
from seven23.models.goals.serializers import GoalsSerializer

from seven23.api.permissions import CanWriteAccount, IsPaid

from rest_framework import permissions
from rest_framework.decorators import permission_classes

import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework_bulk import BulkModelViewSet

class GoalsFilter(django_filters.rest_framework.FilterSet):
    last_edited = django_filters.IsoDateTimeFilter(lookup_expr='gt')
    class Meta:
        model = Goals
        fields = ['account', 'last_edited']


class ApiGoals(BulkModelViewSet):
    serializer_class = GoalsSerializer
    permission_classes = (permissions.IsAuthenticated, CanWriteAccount, IsPaid)
    filter_backends = (DjangoFilterBackend,)
    filter_class = GoalsFilter

    def get_queryset(self):
        queryset = Goals.objects.filter(
            account__in=list(chain(
                self.request.user.accounts.values_list('id', flat=True),
                self.request.user.guests.values_list('account__id', flat=True)
            ))
        )
        last_edited = self.request.query_params.get('last_edited', None)
        if last_edited is None:
            queryset = queryset.filter(deleted=False)
        return queryset