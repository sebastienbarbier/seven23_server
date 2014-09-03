from django.conf.urls import patterns, url, include
from rest_framework import routers

from django_723e.api.v1.accounts.views import api_accounts, api_users
from django_723e.api.v1.currencies.views import api_currencies
from django_723e.api.v1.transactions.views import api_categories, api_transaction, api_cheque, api_change, api_transfert


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'accounts', api_accounts)
router.register(r'currencies', api_currencies)
router.register(r'users', api_users)
router.register(r'categories', api_categories)
router.register(r'transactions', api_transaction)
router.register(r'cheques', api_cheque)
router.register(r'changes', api_change)
router.register(r'transferts', api_transfert)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_723e.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),api_user
    # url(r'accounts/$', api_accounts, name='api.accounts'),

	url(r'^', include(router.urls)),

)
