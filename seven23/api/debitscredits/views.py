"""
    Views for api/va/transactions
"""
from itertools import chain
import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions
from rest_framework_bulk import BulkModelViewSet

from seven23.models.transactions.models import DebitsCredits
from seven23.models.transactions.serializers import DebitsCreditsSerializer
from seven23.api.permissions import CanWriteAccount, IsPaid

class DebitscreditsFilter(django_filters.rest_framework.FilterSet):
    last_edited = django_filters.IsoDateTimeFilter(lookup_expr='gt')
    class Meta:
        model = DebitsCredits
        fields = ['account', 'last_edited']


class ApiDebitscredits(BulkModelViewSet):
    serializer_class = DebitsCreditsSerializer
    permission_classes = (permissions.IsAuthenticated, CanWriteAccount, IsPaid)
    filter_backends = (DjangoFilterBackend,)
    filter_class = DebitscreditsFilter

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return DebitsCredits.objects.none()

        queryset = DebitsCredits.objects.filter(
            account__in=list(chain(
                self.request.user.accounts.values_list('id', flat=True),
                self.request.user.guests.values_list('account__id', flat=True)
            ))
        )
        last_edited = self.request.query_params.get('last_edited', None)

        if last_edited is None:
            queryset = queryset.filter(deleted=False)

        if self.request.method == 'DELETE' and isinstance(self.request.data, list):
            queryset = queryset.filter(id__in=self.request.data)

        return queryset

    def allow_bulk_destroy(self, qs, filtered):

        if isinstance(self.request.data, list):
            return True
        return False