"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework import routers

from seven23 import settings
from seven23.api.categories.views import ApiCategories

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', ApiCategories, base_name='categories')

urlpatterns = ROUTER.urls