"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework import routers

from seven23.api.events.views import ApiEvent

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', ApiEvent, base_name='events')

urlpatterns = ROUTER.urls
