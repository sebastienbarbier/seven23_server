"""
    Main parth.
"""
from django.conf import settings
from django.conf.urls import url, include
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
    # url(r'^$', 'seven23.views.home', name='home'),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^$', views.home, name='home'),
    url(r'^legals/$', views.legals, name='legals'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include("seven23.api.urls")),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)