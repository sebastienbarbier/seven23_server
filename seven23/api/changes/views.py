"""
    Views for api/va/transactions
"""
from itertools import chain
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework_bulk import BulkModelViewSet

from seven23.models.transactions.models import Change
from seven23.models.transactions.serializers import ChangeSerializer
from seven23.api.permissions import CanWriteAccount, IsPaid

class ChangesFilter(django_filters.rest_framework.FilterSet):
    last_edited = django_filters.IsoDateTimeFilter(lookup_expr='gt')
    class Meta:
        model = Change
        fields = ['account', 'last_edited']

#
# List of entry points Category, DebitsCredits, Change
#

class ApiChange(BulkModelViewSet):
    """
        Deliver Change objects
    """
    serializer_class = ChangeSerializer
    permission_classes = (permissions.IsAuthenticated, CanWriteAccount, IsPaid)
    filter_backends = (DjangoFilterBackend,)
    filter_class = ChangesFilter

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Change.objects.none()

        queryset = Change.objects.filter(
            account__in=list(chain(
                self.request.user.accounts.values_list('id', flat=True),
                self.request.user.guests.values_list('account__id', flat=True)
            ))
        )

        last_edited = self.request.query_params.get('last_edited', None)
        if last_edited is None:
            queryset = queryset.filter(deleted=False)

        return queryset

    def allow_bulk_destroy(self, qs, filtered):
        return False