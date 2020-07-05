"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework_bulk.routes import BulkRouter

from seven23.api.changes.views import ApiChange

ROUTER = BulkRouter(trailing_slash=False)
ROUTER.register(r'^', ApiChange, basename='changes')

urlpatterns = ROUTER.urls