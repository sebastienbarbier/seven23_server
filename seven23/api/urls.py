"""
	urls.py : routes from api/
"""
from django.urls import include, path
from django.contrib import admin

from rest_framework.authtoken import views
from rest_framework import routers

from seven23.api.views import api_init
from seven23.api.users.views import revoke_token, email
from seven23.api.saas.views import ApiCharge, ApiCoupon

from seven23 import settings

admin.autodiscover()

urlpatterns = [
    # Get token from username and password
    path(r'api-token-auth', views.obtain_auth_token),
    # Get server instance configurations: api_version, allow_account_creation, id, is_authenticated
    path(r'init', api_init, name='api.init'),
    # Accounts from allauth
    path(r'accounts/',        include('allauth.urls')),
    # Set of entrypoint for v1
    path(r'v1/accounts',      include('seven23.api.accounts.urls')),
    path(r'v1/categories',    include('seven23.api.categories.urls')),
    path(r'v1/changes',       include('seven23.api.changes.urls')),
    path(r'v1/currencies',    include('seven23.api.currencies.urls')),
    path(r'v1/goals',         include('seven23.api.goals.urls')),
    path(r'v1/debitscredits', include('seven23.api.debitscredits.urls')),
    path(r'v1/users/token', revoke_token, name='api.token'),
    path(r'v1/users/email', email, name='api.email'),

    path(r'v1/rest-auth/',    include('rest_auth.urls')),
]

# If creation creation is allowed
if settings.ALLOW_ACCOUNT_CREATION:

    urlpatterns = urlpatterns + [
        path(r'v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    ]

if settings.SAAS:
    urlpatterns = urlpatterns + [
        path(r'v1/payment', ApiCharge, name='api.payment'),
        path(r'v1/coupon/<int:product_id>/<slug:coupon_code>', ApiCoupon, name='api.coupon'),
    ]