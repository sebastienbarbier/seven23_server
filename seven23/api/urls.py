"""
	urls.py : routes from api/
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.authtoken import views
from rest_framework import routers

from seven23.api.views import api_init
from seven23.api.users.views import revoke_token, email

from seven23 import settings

admin.autodiscover()

urlpatterns = [
    # Get token from username and password
    url(r'api-token-auth', views.obtain_auth_token),
    # Get server instance configurations: api_version, allow_account_creation, id, is_authenticated
    url(r'init$', api_init, name='api.init'),
    # Accounts from allauth
    url(r'^accounts/',        include('allauth.urls')),
    # Set of entrypoint for v1
    url(r'^v1/accounts',      include('seven23.api.accounts.urls')),
    url(r'^v1/categories',    include('seven23.api.categories.urls')),
    url(r'^v1/changes',       include('seven23.api.changes.urls')),
    url(r'^v1/currencies',    include('seven23.api.currencies.urls')),
    url(r'^v1/debitscredits', include('seven23.api.debitscredits.urls')),
    url(r'^v1/users/token$', revoke_token, name='api.token'),
    url(r'^v1/users/email$', email, name='api.email'),

    url(r'^v1/rest-auth/',    include('rest_auth.urls')),
]

# If creation creation is allowed
if settings.ALLOW_ACCOUNT_CREATION:

    urlpatterns = urlpatterns + [
        url(r'v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    ]
