"""
    Root views of api
"""

import json
import os
import markdown2
from django.http import HttpResponse

from django.db import models
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from seven23 import settings
from seven23.models.terms.models import TermsAndConditions
from seven23.models.rest_auth.serializers import UserSerializer

from allauth.account.models import EmailAddress

@api_view(['POST'])
def email(request):
    """
        Revoke user token
    """
    try:
        email = EmailAddress.objects.get(user=request.user)
        email.email = request.data['email']
        email.primary = True
        email.save()

        request.user.email = request.data['email']
        request.user.save()
    except EmailAddress.DoesNotExist:
        EmailAddress.objects.create(
            user = request.user,
            primary = True,
            email = request.data['email'])

        request.user.email = request.data['email']
        request.user.save()

    # Return json format string.
    j = json.dumps(UserSerializer(request.user).data, separators=(',', ':'))
    return HttpResponse(j, content_type='application/json')


@api_view(["DELETE"])
def revoke_token(request):
    """
        Revoke user token
    """
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
    except:
        return HttpResponse(status=404)

    return HttpResponse(status=200)