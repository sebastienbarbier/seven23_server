
from datetime import datetime
from seven23.models.profile.models import Profile
from rest_framework.authentication import TokenAuthentication
from seven23.models.stats.models import MonthlyActiveUser, DailyActiveUser

def active_user_middleware(get_response):

    def middleware(request):
        user = request.user

        user_auth_tuple = TokenAuthentication().authenticate(request)
        if user_auth_tuple is not None:
            (user, token) = user_auth_tuple

            if user.is_authenticated and not user.is_superuser:

                # If user has no profile, we create on.
                if not hasattr(user, 'profile'):
                    Profile.objects.create(user=user)

                now = datetime.now()
                last_api_call = user.profile.last_api_call
                udpate_user = False

                if now.year != last_api_call.year or now.month != last_api_call.month :
                    MonthlyActiveUser.objects.update_or_create(year=now.year, month=now.month)
                    udpate_user = True

                if now.year != last_api_call.year or now.month != last_api_call.month or now.day != last_api_call.day :
                    DailyActiveUser.objects.update_or_create(year=now.year, month=now.month, day=now.day)
                    udpate_user = True

                if udpate_user:
                    user.profile.last_api_call = now
                    user.save()

        # Perform actual request
        response = get_response(request)

        return response

    return middleware