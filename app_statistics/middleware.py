from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import MainStatistics, QueryStatistics


def MainUserStatisticsMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        if request.user.is_authenticated:
            main_record = MainStatistics()
            main_record.user = request.user
            main_record.url = request.path
            main_record.ip = request.META['HTTP_X_REAL_IP'] if request.META.get('HTTP_X_REAL_IP', False) \
                else request.META['REMOTE_ADDR']
            main_record.browser = request.META['HTTP_USER_AGENT'] if request.META.get('HTTP_USER_AGENT', False) else 0
            main_record.session_key = Session.objects.get(session_key=request.session.session_key)
            main_record.dactivity = timezone.now()
            main_record.save()
            if 'get' in request.path:
                filter = dict(request.GET)
                keys = []
                for k in filter.keys():
                    keys.append(k)
                for key in keys:
                    if filter[key] == [''] or (key == 'draw') or ('columns' in key) or ('order' in key) \
                            or (key == 'start') or (key == 'length') or ('search' in key) or (key == '_'):
                        filter.pop(key)
                if filter:
                    query_record = QueryStatistics()
                    query_record.app_stat = MainStatistics.objects.last()
                    query_record.filter = filter
                    query_record.save()
        return response
    return middleware
