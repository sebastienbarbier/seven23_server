"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework_bulk.routes import BulkRouter

from seven23 import settings
from seven23.api.accounts.views import AccountsList

ROUTER = BulkRouter(trailing_slash=False)
ROUTER.register(r'^', AccountsList, base_name='accounts')

urlpatterns = ROUTER.urls