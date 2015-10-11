from django.conf.urls import patterns, include, url
from django.contrib import admin
from django_723e.api.views import api_init

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_723e.views.home', name='home'),
    url(r'api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'init/$', api_init, name='api.init'),
    url(r'^v1/', include("django_723e.api.v1.urls")),
)
