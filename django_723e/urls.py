"""
    Main parth.
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view

from . import views

admin.autodiscover()

urlpatterns = [

    # Examples:
    # url(r'^$', 'django_723e.views.home', name='home'),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include("django_723e.api.urls")),
    url(r'^docs/', get_swagger_view(title='723e API')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
