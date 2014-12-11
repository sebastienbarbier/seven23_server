from django.conf.urls import patterns, url, include
from rest_framework import routers

from django_723e.api.v1.accounts.views import api_accounts, api_users
from django_723e.api.v1.currencies.views import api_currencies
from django_723e.api.v1.transactions.views import api_categories, api_debitscredits, api_cheque, api_change, api_transfert
from django_723e.api.v1.views import resume_year

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'accounts', api_accounts)
router.register(r'currencies', api_currencies)
router.register(r'users', api_users)
router.register(r'categories', api_categories)
router.register(r'debitscredits', api_debitscredits)
router.register(r'cheques', api_cheque)
router.register(r'changes', api_change)
router.register(r'transferts', api_transfert)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_723e.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),api_user
    # url(r'accounts/$', api_accounts, name='api.accounts'),

	url(r'resume_year/$', resume_year, name='resume_current_year'),
	url(r'resume_year/(?P<year>[0-9]+)/$', resume_year, name='resume_specific_year'),
	url(r'^', include(router.urls)),

)
