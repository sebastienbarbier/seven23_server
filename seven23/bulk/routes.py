import copy

from rest_framework.routers import DefaultRouter, SimpleRouter


class BulkRouter(DefaultRouter):
    """
    Map PUT/PATCH/DELETE on the list route to bulk viewset actions.

    Viewsets are registered with prefix '^' so detail routes keep the
    '/{pk}' separator when included under a path without a trailing slash
    (e.g. path('v1/accounts', include(...))).
    """

    routes = copy.deepcopy(SimpleRouter.routes)
    routes[0].mapping.update({
        'put': 'bulk_update',
        'patch': 'partial_bulk_update',
        'delete': 'bulk_destroy',
    })
