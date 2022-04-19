"""
    Main views
"""
import markdown2
import datetime
import calendar
from seven23 import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone

from seven23.models.saas.models import Product
from seven23.models.terms.models import TermsAndConditions

def home(request):
    return render(request, 'self-hosted.html', {})

def paid(request):

    def add_months(sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year,month)[1])
        return timezone.make_aware(datetime.datetime(year, month, day, sourcedate.hour, sourcedate.minute, sourcedate.second))

    if request.method == "POST":
        user = User.objects.get(pk=request.POST['user'])
        user.profile.valid_until = add_months(timezone.now(), 6)
        user.save()

        url = request.POST['url']

        return render(request, 'paid.html', { "user": user, "url": url })
    else:
        return HttpResponseNotFound("Page not found")

def robots(request):
    return render(request, 'robots/robots-self-hosted.txt', content_type="text/plain")