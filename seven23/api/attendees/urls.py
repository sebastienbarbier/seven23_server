"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework import routers

from seven23.api.attendees.views import ApiAttendee

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', ApiAttendee, base_name='attendees')

urlpatterns = ROUTER.urls
