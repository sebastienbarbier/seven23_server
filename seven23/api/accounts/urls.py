"""
    Define urls for api/v1
"""

from seven23.bulk import BulkRouter

from seven23.api.accounts.views import AccountsList

ROUTER = BulkRouter(trailing_slash=False)
ROUTER.register(r'^', AccountsList, basename='accounts')

urlpatterns = ROUTER.urls
