"""
    Define urls for api/v1
"""

from rest_framework_bulk.routes import BulkRouter

from seven23 import settings
from seven23.api.goals.views import ApiGoals

ROUTER = BulkRouter(trailing_slash=False)
ROUTER.register(r'^', ApiGoals, base_name='goals')

urlpatterns = ROUTER.urls