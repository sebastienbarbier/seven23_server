"""
Bulk create/update/destroy helpers for Django REST Framework.

Adapted from the MIT-licensed djangorestframework-bulk (Miroslav Shubernetskiy),
which is no longer maintained. Kept as an in-repo module so the public API
used by seven23 clients stays compatible.
"""

from .generics import BulkModelViewSet
from .mixins import BulkCreateModelMixin, BulkDestroyModelMixin, BulkUpdateModelMixin
from .routes import BulkRouter
from .serializers import BulkListSerializer, BulkSerializerMixin

__all__ = [
    'BulkCreateModelMixin',
    'BulkDestroyModelMixin',
    'BulkListSerializer',
    'BulkModelViewSet',
    'BulkRouter',
    'BulkSerializerMixin',
    'BulkUpdateModelMixin',
]
