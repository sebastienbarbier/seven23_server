from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from django.contrib import admin

from rest_framework import routers

from django_723e.api.v1.accounts.views import api_accounts

admin.autodiscover()

urlpatterns = [

    # Examples:
    # url(r'^$', 'django_723e.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	# url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	# url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS

    url(r'^api/', include("django_723e.api.urls")),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
