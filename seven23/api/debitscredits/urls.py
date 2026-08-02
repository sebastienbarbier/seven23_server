"""
    Define urls for api/v1
"""

from seven23.bulk import BulkRouter

from seven23.api.debitscredits.views import ApiDebitscredits

ROUTER = BulkRouter(trailing_slash=False)
ROUTER.register(r'^', ApiDebitscredits, basename='debitscredits')

urlpatterns = ROUTER.urls
