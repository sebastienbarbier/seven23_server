"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework import routers

from django_723e import settings
from django_723e.api.changes.views import ApiChange

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', ApiChange, base_name='changes')

urlpatterns = ROUTER.urls
