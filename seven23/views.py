"""
    Main views
"""
import markdown2
from seven23 import settings
from django.http import HttpResponse
from django.shortcuts import render

from seven23.models.saas.models import Product
from seven23.models.terms.models import TermsAndConditions

def home(request):
    return render(request, 'self-hosted.html', {})

def robots(request):
    return render(request, 'robots/robots-self-hosted.txt', content_type="text/plain")