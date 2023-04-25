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
from seven23.models.saas.serializers import ProductSerializer
from seven23.models.saas.models import Product

from allauth.account.models import EmailAddress

@api_view(["GET"])
def api_init(request):
    """
        Return status on client initialisation
    """
    result = {}

    # Return API Version.
    result['version'] = settings.VERSION
    result['api_version'] = settings.API_VERSION
    result['saas'] = settings.SAAS
    result['allow_account_creation'] = settings.ALLOW_ACCOUNT_CREATION
    result['contact'] = settings.CONTACT_EMAIL

    if result['saas']:
        result['products'] = ProductSerializer(list(Product.objects.all()), many=True).data
        result['trial_period'] = settings.TRIAL_PERIOD
        result['stripe_key'] = settings.STRIPE_PUBLIC_KEY

    try:
        terms = TermsAndConditions.objects.latest('date')
        result['terms_and_conditions_date'] = terms.date.strftime("%Y-%m-%d")
        result['terms_and_conditions'] = markdown2.markdown(terms.markdown)
    except TermsAndConditions.DoesNotExist:
       result['terms_and_conditions_date'] = None
       result['terms_and_conditions'] = None

    # Return json format string.
    j = json.dumps(result, separators=(',', ':'))
    return HttpResponse(j, content_type='application/json')