"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework import routers

from seven23 import settings
from seven23.api.accounts.views import AccountsList

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', AccountsList, base_name='accounts')

urlpatterns = ROUTER.urls