"""
    Views for api/va/transactions
"""
from itertools import chain
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_bulk import BulkModelViewSet

from seven23.models.categories.models import Category
from seven23.models.categories.serializers import CategorySerializer
from seven23.api.permissions import CanWriteAccount, IsPaid

class CategoriesFilter(django_filters.rest_framework.FilterSet):
    last_edited = django_filters.IsoDateTimeFilter(lookup_expr='gt')
    class Meta:
        model = Category
        fields = ['account', 'last_edited']

class ApiCategories(BulkModelViewSet):
    """
        Deliver Categor model object
    """
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated, CanWriteAccount, IsPaid)
    filter_backends = (DjangoFilterBackend,)
    filter_class = CategoriesFilter

    def get_queryset(self):

        if self.request.user.is_anonymous:
            return Category.objects.none()

        queryset = Category.objects.filter(
            account__in=list(chain(
                self.request.user.accounts.values_list('id', flat=True),
                self.request.user.guests.values_list('account__id', flat=True)
            ))
        )

        last_edited = self.request.query_params.get('last_edited', None)
        if last_edited is None:
            queryset = queryset.filter(deleted=False)

        return queryset


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(CategorySerializer(instance).data)