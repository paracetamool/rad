from django.contrib.auth.models import User
from .models import Profile
from datetime import datetime, timedelta
from django.utils import timezone

tz = timezone.get_default_timezone()


def LastUserActivityMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        if request.user.is_authenticated:
            Profile.objects.filter(user=request.user.pk).update(last_activity=datetime.now(tz))
            if request.user.profile.is_online is False:
                Profile.objects.filter(user=request.user.pk).update(is_online=True)
        return response
    return middleware


def CurrentUsersStatusMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            inner_qs = list(Profile.objects.exclude(is_online=False).values_list('user', flat=True))
            users = User.objects.exclude(is_active=False).filter(pk__in=inner_qs)
            for elem in users.iterator():
                if elem.profile.last_activity is not None:
                    if elem.profile.last_activity.astimezone(tz) + timedelta(minutes=10) < datetime.now(tz):
                        Profile.objects.filter(user=elem.pk).update(is_online=False)
        return response
    return middleware
