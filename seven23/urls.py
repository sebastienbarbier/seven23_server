"""
    Main parth.
"""
from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

admin.autodiscover()

schema_view = get_schema_view(
   openapi.Info(
      title="Seven23 API",
      default_version='v1',
      description="<strong>To use authentication</strong>, click on the authorize button and set value <code>Token ADD_YOUR_TOKEN_HERE</code>.<br />Key can be found calling <code>/api-token-auth</code> or in-app at the <em>setting server</em> section.",
      contact=openapi.Contact(email="seven23@sebastienbarbier.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    # Examples:
    # re_path(r'^$', 'seven23.views.home', name='home'),
    # re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^$', views.home, name='home'),
    re_path(r'^legals/$', views.legals, name='legals'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include("seven23.api.urls")),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^robots.txt$', views.robots, name='robots'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)