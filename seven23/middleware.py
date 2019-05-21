
from datetime import datetime
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication

from seven23 import settings

def maintenance_middleware(get_response):

    def middleware(request):
        if settings.MAINTENANCE and request.path.startswith('/api'):
            user_auth_tuple = TokenAuthentication().authenticate(request)
            if user_auth_tuple is not None:
                (user, token) = user_auth_tuple

                if not user.is_superuser:
                    return HttpResponse(status=503)
            else:
                return HttpResponse(status=503)

        # Perform actual request
        response = get_response(request)
        return response

    return middleware