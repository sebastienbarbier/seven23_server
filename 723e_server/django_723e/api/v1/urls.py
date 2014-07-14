from django.conf.urls import patterns, url

from django.contrib import admin

from django_723e.api.v1.accounts.views import api_login
from django_723e.api.v1.transactions.views import api_transactions

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_723e.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'login/$', api_login, name='api.v1.login'),
    url(r'transactions/?$', api_transactions.as_view(), name='my_crud_view'),

)
