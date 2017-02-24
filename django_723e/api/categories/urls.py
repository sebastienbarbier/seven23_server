"""
    Define urls for api/v1
"""

from django.conf.urls import url, include

from rest_framework import routers

from django_723e import settings
from django_723e.api.categories.views import ApiCategories

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'^', ApiCategories, base_name='categories')

urlpatterns = ROUTER.urls