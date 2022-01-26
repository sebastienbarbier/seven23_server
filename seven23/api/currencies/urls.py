"""
    Define urls for api/v1
"""

from django.urls import include

from rest_framework import routers

from seven23 import settings
from seven23.api.currencies.views import CurrenciesList

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', CurrenciesList, basename='currencies')

urlpatterns = ROUTER.urls