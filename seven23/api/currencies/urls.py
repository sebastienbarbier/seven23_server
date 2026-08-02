"""
    Define urls for api/v1
"""

from rest_framework.routers import DefaultRouter

from seven23.api.currencies.views import CurrenciesList

ROUTER = DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', CurrenciesList, basename='currencies')

urlpatterns = ROUTER.urls
