"""
    Root views of api
"""

import json
from django.http import HttpResponse

from rest_framework.decorators import api_view

from django_723e import settings

@api_view(["GET"])
def api_init(request):
    """
        Return status on client initialisation
    """
    result = {}

    # Return API Version.
    result['api_version'] = [1, 1, 0]
    result['allow_account_creation'] = settings.ALLOW_ACCOUNT_CREATION

    if request.user.is_authenticated():
        result['is_authenticated'] = True
        # If user is authentificated, we return some details which might
        # be usefull like displaying name, or sending mail.
        result['id'] = request.user.id
        # result['username'] = request.user.username
        # result['first_name'] = request.user.first_name
        # result['last_name'] = request.user.last_name
        # result['email'] = request.user.email
    else:
        result['is_authenticated'] = False

    # Return json format string.
    j = json.dumps(result, separators=(',', ':'))
    return HttpResponse(j, content_type='application/json')
