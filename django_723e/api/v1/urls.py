"""
    Define urls for api/v1
"""

from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from rest_framework import routers

from django_723e.api.v1.accounts.views import api_accounts, api_users, subscription
from django_723e.api.v1.currencies.views import api_currencies
from django_723e.api.v1.transactions.views import api_categories, api_debitscredits, api_change

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'accounts', api_accounts)
ROUTER.register(r'currencies', api_currencies)
ROUTER.register(r'users', api_users)
ROUTER.register(r'categories', api_categories)
ROUTER.register(r'debitscredits', api_debitscredits)
ROUTER.register(r'changes', api_change)

urlpatterns = [
    url(r'subscription/$', subscription, name='subscription'),

    # URL used to send mail
    url(r'rest-auth/', include('rest_auth.urls')),
    # Change Password
    url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'reset/complete/$',
        auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^', include(ROUTER.urls)),
]
