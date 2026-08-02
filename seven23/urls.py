"""
    Main path.
"""
from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)

from . import views
from .logs import print_settings_report

admin.autodiscover()

# Print settings errors load for easier deployment
print_settings_report()

urlpatterns = [

    # Examples:
    # re_path(r'^$', 'seven23.views.home', name='home'),
    # re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^$', views.home, name='home'),
    re_path(r'^paid/', views.paid, name='paid'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include("seven23.api.urls")),
    re_path(r'^schema/$', SpectacularAPIView.as_view(), name='schema'),
    re_path(r'^swagger\.json$', SpectacularAPIView.as_view(), name='schema-json'),
    re_path(r'^swagger\.yaml$', SpectacularYAMLAPIView.as_view(), name='schema-yaml'),
    re_path(r'^swagger/$', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-swagger-ui'),
    re_path(r'^redoc/$', SpectacularRedocView.as_view(url_name='schema'), name='schema-redoc'),
    re_path(r'^robots.txt$', views.robots, name='robots'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
