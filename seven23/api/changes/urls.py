"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework import routers

from seven23 import settings
from seven23.api.changes.views import ApiChange

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', ApiChange, base_name='changes')

urlpatterns = ROUTER.urls
