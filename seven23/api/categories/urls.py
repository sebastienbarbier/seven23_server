"""
    Define urls for api/v1
"""

from seven23.bulk import BulkRouter

from seven23.api.categories.views import ApiCategories

ROUTER = BulkRouter(trailing_slash=False)
ROUTER.register(r'^', ApiCategories, basename='categories')

urlpatterns = ROUTER.urls
