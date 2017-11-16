"""
	urls.py : routes from api/
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.authtoken import views
from rest_framework import routers

from seven23.api.views import api_init, revoke_token

from seven23 import settings

admin.autodiscover()

urlpatterns = [
    # Get token from username and password
    url(r'api-token-auth', views.obtain_auth_token),
    # Get server instance configurations: api_version, allow_account_creation, id, is_authenticated
    url(r'init$', api_init, name='api.init'),
    # Accounts from allauth
    url(r'^accounts/',        include('allauth.urls', namespace='v1')),
    # Set of entrypoint for v1
    url(r'^v1/accounts',      include('seven23.api.accounts.urls', namespace='v1')),
    url(r'^v1/categories',    include('seven23.api.categories.urls', namespace='v1')),
    url(r'^v1/changes',       include('seven23.api.changes.urls', namespace='v1')),
    url(r'^v1/currencies',    include('seven23.api.currencies.urls', namespace='v1')),
    url(r'^v1/debitscredits', include('seven23.api.debitscredits.urls', namespace='v1')),
    url(r'^v1/events',        include('seven23.api.events.urls', namespace='v1')),
    url(r'^v1/attendees',     include('seven23.api.attendees.urls', namespace='v1')),
    url(r'^v1/token/revoke$', revoke_token, name='token.revoke'),

    url(r'^v1/rest-auth/',    include('rest_auth.urls', namespace='v1')),
]

# If creation creation is allowed
if settings.ALLOW_ACCOUNT_CREATION:

    urlpatterns = urlpatterns + [
        url(r'v1/rest-auth/registration/', include('rest_auth.registration.urls'), name='fb_login'),
    ]
