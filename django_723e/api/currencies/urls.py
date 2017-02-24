"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework import routers

from django_723e import settings
from django_723e.api.currencies.views import CurrenciesList

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', CurrenciesList, base_name='currencies')

urlpatterns = ROUTER.urls