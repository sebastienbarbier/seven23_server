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
from django import forms

from seven23.models.saas.models import Product
from seven23.models.terms.models import TermsAndConditions
from seven23.models.currency.models import Currency
from seven23.models.users.forms import SuperUserForm

def home(request):

    form = SuperUserForm()

    # We manage form if POST request before initialising states
    if request.method == "POST":
        form = SuperUserForm(request.POST)

        # If form is valid we save it
        if form.is_valid():
            try:
                form.save()
            except forms.ValidationError as e:
                # If we receive ValidationError, it means a superuser already exist, we can ignore
                pass

    # We define current states
    is_database_ready = True
    is_fixtures_loaded = None
    is_superuser_created = None

    # We check is user objects exist,otherwise raise Exception Value: no such table: auth_user
    try:
        User.objects.all().exists()
    except:
        is_database_ready = False

    # If currencies exits, we assume that fixtures are loaded
    if is_database_ready:
        is_fixtures_loaded = Currency.objects.count() != 0

    # If there is no user, it means that no superuser has been created
    if is_database_ready and is_fixtures_loaded:
        is_superuser_created = User.objects.count() != 0

    return render(request, 'self-hosted.html', {
        'settings': settings,
        'form': form,
        'user': request.user,
        'is_database_ready': is_database_ready,
        'is_fixtures_loaded': is_fixtures_loaded,
        'is_superuser_created': is_superuser_created,
    })

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