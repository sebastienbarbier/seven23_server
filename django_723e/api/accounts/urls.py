"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework import routers

from django_723e import settings
from django_723e.api.accounts.views import AccountsList

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', AccountsList, base_name='accounts')

urlpatterns = ROUTER.urls