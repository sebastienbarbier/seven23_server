from rest_framework.viewsets import ModelViewSet

from .mixins import BulkCreateModelMixin, BulkDestroyModelMixin, BulkUpdateModelMixin


class BulkModelViewSet(
    BulkCreateModelMixin,
    BulkUpdateModelMixin,
    BulkDestroyModelMixin,
    ModelViewSet,
):
    """ModelViewSet with bulk create, update, and destroy on the collection."""
