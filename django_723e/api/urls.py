"""
	urls.py : routes from api/
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.authtoken import views
from rest_framework import routers

from django_723e.api.views import api_init

from django_723e import settings

admin.autodiscover()

urlpatterns = [
    # Get token from username and password
    url(r'api-token-auth', views.obtain_auth_token),
    # Get server instance configurations: api_version, allow_account_creation, id, is_authenticated
    url(r'init$', api_init, name='api.init'),
    # Accounts from allauth
    url(r'^accounts/',        include('allauth.urls', namespace='v1')),
    # Set of entrypoint for v1
    url(r'^v1/accounts',      include('django_723e.api.accounts.urls', namespace='v1')),
    url(r'^v1/categories',    include('django_723e.api.categories.urls', namespace='v1')),
    url(r'^v1/changes',       include('django_723e.api.changes.urls', namespace='v1')),
    url(r'^v1/currencies',    include('django_723e.api.currencies.urls', namespace='v1')),
    url(r'^v1/debitscredits', include('django_723e.api.debitscredits.urls', namespace='v1')),

    url(r'^v1/rest-auth/',    include('rest_auth.urls', namespace='v1')),
]

# If creation creation is allowed
if settings.ALLOW_ACCOUNT_CREATION:

    urlpatterns = urlpatterns + [
        url(r'v1/rest-auth/registration/', include('rest_auth.registration.urls'), name='fb_login'),
    ]
