from django.conf.urls import patterns, include, url

from django.contrib import admin

from django_723e.home.views import homepage
from django_723e.dashboard.views import dashboard, details, liste

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_723e.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', homepage, name='homepage'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^dashboard/liste/$', liste, name='liste'),
    url(r'^dashboard/details/$', details, name='details'),

    url(r'^api/', include("django_723e.api.urls")),

    url(r'^admin/', include(admin.site.urls)),
)