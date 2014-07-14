from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_723e.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/', include("django_723e.api.urls")),

    url(r'^admin/', include(admin.site.urls)),
)
