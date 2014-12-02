# -*- coding: utf-8 -*-

import json
from django.http import HttpResponse

from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token

from django.core import serializers

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(["GET"])
def api_init(request):
    result = {}

    # Return API Version.
    result['api_version'] = "1.0.0"

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
    j = json.dumps(result, separators=(',',':'))
    return HttpResponse(j, content_type='application/json')
