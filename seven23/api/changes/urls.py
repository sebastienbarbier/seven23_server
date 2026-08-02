"""
    Define urls for api/v1
"""

from seven23.bulk import BulkRouter

from seven23.api.changes.views import ApiChange

ROUTER = BulkRouter(trailing_slash=False)
ROUTER.register(r'^', ApiChange, basename='changes')

urlpatterns = ROUTER.urls
