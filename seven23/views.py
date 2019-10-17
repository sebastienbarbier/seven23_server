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
    """
        Home page when trying to open server URL.
        Should confirm everything is ok, and provide a link to a client.
    """
    if settings.SAAS:

        photos = [
            {
                "small": "images/screenshots/small/01-dashboard-desktop-light.png",
                "large": "images/screenshots/large/01-dashboard-desktop-light.png",
                "alt": "Seven23 dashboard desktop"
            },
            {
                "small": "images/screenshots/small/01-dashboard-mobile-light.png",
                "large": "images/screenshots/large/01-dashboard-mobile-light.png",
                "alt": "Seven23 dashboard mobile"
            },
            {
                "small": "images/screenshots/small/01-transactions-desktop-light.png",
                "large": "images/screenshots/large/01-transactions-desktop-light.png",
                "alt": "Seven23 transactions desktop"
            },
            {
                "small": "images/screenshots/small/01-transactions-mobile-light.png",
                "large": "images/screenshots/large/01-transactions-mobile-light.png",
                "alt": "Seven23 transactions mobile"
            },
            {
                "small": "images/screenshots/small/01-categories-desktop-light.png",
                "large": "images/screenshots/large/01-categories-desktop-light.png",
                "alt": "Seven23 categories desktop"
            },
            {
                "small": "images/screenshots/small/01-categories-mobile-light.png",
                "large": "images/screenshots/large/01-categories-mobile-light.png",
                "alt": "Seven23 categories mobile"
            },
            {
                "small": "images/screenshots/small/01-change-desktop-light.png",
                "large": "images/screenshots/large/01-change-desktop-light.png",
                "alt": "Seven23 change desktop"
            },
            {
                "small": "images/screenshots/small/01-change-mobile-light.png",
                "large": "images/screenshots/large/01-change-mobile-light.png",
                "alt": "Seven23 change mobile"
            },
            {
                "small": "images/screenshots/small/01-report-desktop-light.png",
                "large": "images/screenshots/large/01-report-desktop-light.png",
                "alt": "Seven23 report desktop"
            },
            {
                "small": "images/screenshots/small/01-report-mobile-light.png",
                "large": "images/screenshots/large/01-report-mobile-light.png",
                "alt": "Seven23 report mobile"
            }
        ]

        return render(request, 'home.html', {
            "price": Product.objects.all()[0].price,
            "trial": settings.TRIAL_PERIOD,
            "photos": photos
        })
    else:
        return render(request, 'self-hosted.html', {})

def legals(request):
    """
        Home page when trying to open server URL.
        Should confirm everything is ok, and provide a link to a client.
    """
    try:
        terms = TermsAndConditions.objects.latest('date')
        terms = markdown2.markdown(terms.markdown)
    except:
        terms = None

    return render(request, 'legals.html', {"terms": terms})

def robots(request):
    if settings.SAAS:
        return render(request, 'robots/robots-saas.txt', content_type="text/plain")
    else:
        return render(request, 'robots/robots-self-hosted.txt', content_type="text/plain")