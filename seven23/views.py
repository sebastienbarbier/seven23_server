"""
    Main views
"""
import markdown2
from seven23 import settings
from django.http import HttpResponse
from django.shortcuts import render

from seven23.models.terms.models import TermsAndConditions

def home(request):
    """
        Home page when trying to open server URL.
        Should confirm everything is ok, and provide a link to a client.
    """
    return render(request, 'home.html', {"price": settings.PRICE_YEAR, "trial": settings.TRIAL_PERIOD})

def legals(request):
    """
        Home page when trying to open server URL.
        Should confirm everything is ok, and provide a link to a client.
    """

    terms = TermsAndConditions.objects.latest('date')

    return render(request, 'legals.html', {"terms": markdown2.markdown(terms.markdown)})