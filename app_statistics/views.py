import calendar
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Count
from django.utils.timezone import localtime
from django.db.models.functions import TruncHour, TruncDay, TruncMonth, TruncYear

from profiles.models import Profile
from .models import Dcolors, MainStatistics


@login_required(login_url='/login/')
def profile_info(request, pk):
    context = {
        'user': User.objects.get(pk=pk),
        'pages': MainStatistics.objects.filter(user=User.objects.get(pk=pk)).order_by('-dactivity')[0:500]
    }
    return render(request, 'grappelli/profile_info.html', context)


class DataTableData:
    def __init__(self, request=None):
        self.head = [
            {'text': 'Логин'},
            {'text': 'ФИО'},
            {'text': 'Организация'},
            {'text': 'Последняя активность'},
            {'text': 'Cтатус'},
        ]
        self.columns = [
            {
                'name': 'username',
                'field': 'user_id__username',
                'format': lambda val: f'<div><a href="#id_modal_profile_info" data-toggle="modal" onclick="$(\'#id_modal_profile_info\').load(\'/profile_info/{User.objects.get(username=val).pk}/\');">{val}</a></div>',},
            {
                'name': 'full_name',
                'fieldset': ['user_id__last_name', 'user_id__first_name'],
                'constructor': lambda arr: '{0} {1}'.format(*arr),},
            {
                'name': 'org',
                'field': 'org__krat',},
            {
                'name': 'last_activity',
                'format': lambda time: localtime(time).strftime("%d.%m.%Y %H:%M"),},
            {
                'name': 'is_online',
                'format': lambda val: f'<img src="/static/admin/img/icon-{"yes" if val else "no"}.svg" alt="{val}" title="{"В" if val else "Вне"} сети">',},
        ]
        self.enum = True
        self.enum_head = {'data-orderable': 'false', 'text': '№'}
        self.queries = [
            Profile.objects.values('user_id__username', 'user_id__last_name', 'user_id__first_name', 'org__krat', 'last_activity', 'is_online').exclude(user_id__is_active=False),
        ]
        self.base_query = self.queries[0]
        self.query = self.base_query
        self.records_total = self.base_query.count()
        self.request = request
        self.search_values = {
            'context': request.GET['search[value]'],
            'columns': [self.request.GET[f'columns[{i}][search][value]'].split(',') for i in range(int(self.enum), int(self.enum) + len(self.columns))],
        }
        self.search_fields = {
            'context': ['user_id__username', 'user_id__last_name', 'user_id__first_name', 'org__krat', 'last_activity', 'is_online'],
            'columns': ['user_id__username', 'user_id__username', 'org__krat', 'last_activity', 'is_online'],
        }

    def __get_enum_column__(self, i):
        return f'<div>{i + 1}</div>'

    def __get_ordered_query__(self):
        self.__context_filter__()
        direction = {'asc': '', 'desc': '-'}[self.request.GET['order[0][dir]']]
        column = self.columns[int(self.request.GET['order[0][column]']) - int(self.enum)]
        field = column['fieldset'][0] if 'fieldset' in column else column.get('field', column['name'])
        self.query = self.query.order_by(direction + field)

    def __get_col_value__(self, query, col):
        if 'fieldset' in col:
            if 'constructor' in col:
                value = col['constructor']([query[field] for field in col['fieldset']])
            else:
                value = query[col['fieldset'][0]]
        else:
            value = query[col.get('field', col['name'])]
        if 'format' in col:
            value = col['format'](value)
        return value

    def __context_filter__(self):
        value = self.search_values['context']
        reset_query = True
        if value:
            reset_query = False
            out = ''
            for field in self.search_fields['context']:
                qwe = self.query.filter(**{f'{field}__icontains': value})
                out = qwe if not out else out | qwe
            self.query = out
        else:
            for value, field in zip(self.search_values['columns'], self.search_fields['columns']):
                if value != ['']:
                    reset_query = False
                    self.query = self.query.filter(**{f'{field}__in': value})
        if reset_query:
            self.query = self.base_query

    def __get_additions__(self):
        out = {'orgList': list(Profile.objects.values_list(self.columns[2]['field'], flat=True).order_by().distinct())}
        return dict(adds=out)

    def get_table_data(self):
        self.__get_ordered_query__()
        start = int(self.request.GET['start'])
        pages = int(self.request.GET['length'])
        pages = pages if pages + 1 else self.records_total
        body = []
        for i, el in zip(range(start, start + pages), self.query[start:start + pages]):
            row = [] if not self.enum else [self.__get_enum_column__(i)]
            row += [self.__get_col_value__(el, col) for col in self.columns]
            body.append(row)
        data = {'data': body, 'draw': self.request.GET.get('draw', 0), 'recordsTotal': self.records_total, 'recordsFiltered': self.query.count(), **self.__get_additions__()}
        return data


def get_users_data(request):
    return JsonResponse(DataTableData(request).get_table_data())


def get_traffic_data(request):
    type_user, users, response = request.GET['select_type_user'], [], {}

    if request.GET['select_type_date'] == 'hour_day':
        input_year, input_month, input_day, response['labels'], response['dict_stacked'] = \
            request.GET['input_date'].split('-')[0], request.GET['input_date'].split('-')[1], \
            request.GET['input_date'].split('-')[2], list(range(24)), dict()
        inner_qs = list(User.objects.values_list('username', flat=True)) if type_user == 'Все' \
            else list(User.objects.filter(groups__name=type_user).values_list('username', flat=True))
        visits = MainStatistics.objects.filter(user__in=inner_qs, dactivity__year=input_year,
                                               dactivity__month=input_month, dactivity__day=input_day)
        for elem in visits.values('user').order_by().distinct():
            users.append(elem['user'])
        for param in users:
            y_tmp = [0] * len(response['labels'])
            groups = visits.filter(user=param).annotate(hour=TruncHour('dactivity')).values('hour').annotate(
                visits=Count('id')).order_by()
            for elem in groups:
                for data in response['labels']:
                    if int(localtime(elem['hour']).strftime('%H')) == data:
                        y_tmp[response['labels'].index(data)] = elem['visits']
            response['dict_stacked'][param] = y_tmp, Profile.objects.get(user__username=param).color

    if request.GET['select_type_date'] == 'day_week':
        input_year, input_week, response['labels'], response['dict_stacked'] = \
            request.GET['input_date'].replace('W', '').split('-')[0], \
            request.GET['input_date'].replace('W', '').split('-')[1], \
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], dict()
        inner_qs = list(User.objects.values_list('username', flat=True)) if type_user == 'Все' \
            else list(User.objects.filter(groups__name=type_user).values_list('username', flat=True))
        visits = MainStatistics.objects.filter(user__in=inner_qs, dactivity__year=input_year,
                                               dactivity__week=input_week)
        for elem in visits.values('user').order_by().distinct():
            users.append(elem['user'])
        for param in users:
            y_tmp = [0] * len(response['labels'])
            groups = visits.filter(user=param).annotate(day=TruncDay('dactivity')).values('day').annotate(
                visits=Count('id')).order_by()
            for elem in groups:
                for data in response['labels']:
                    if localtime(elem['day']).strftime('%A') == data:
                        y_tmp[response['labels'].index(data)] = elem['visits']
            response['dict_stacked'][param] = y_tmp, Profile.objects.get(user__username=param).color

    if request.GET['select_type_date'] == 'day_month':
        input_year, input_month = request.GET['input_date'].split('-')[0], request.GET['input_date'].split('-')[1]
        response['labels'], response['dict_stacked'] = \
            list(range(1, calendar.monthrange(int(input_year), int(input_month))[1] + 1)), dict()
        inner_qs = list(User.objects.values_list('username', flat=True)) if type_user == 'Все' \
            else list(User.objects.filter(groups__name=type_user).values_list('username', flat=True))
        visits = MainStatistics.objects.filter(user__in=inner_qs, dactivity__year=input_year,
                                               dactivity__month=input_month)
        for elem in visits.values('user').order_by().distinct():
            users.append(elem['user'])
        for param in users:
            y_tmp = [0] * len(response['labels'])
            groups = visits.filter(user=param).annotate(day=TruncDay('dactivity')).values('day').annotate(
                visits=Count('id')).order_by()
            for elem in groups:
                for data in response['labels']:
                    if int(localtime(elem['day']).strftime('%d')) == data:
                        y_tmp[response['labels'].index(data)] = elem['visits']
            response['dict_stacked'][param] = y_tmp, Profile.objects.get(user__username=param).color

    if request.GET['select_type_date'] == 'month_year':
        input_year, response['labels'], response['dict_stacked'] = request.GET['input_date'], \
                                                                   ['January', 'February', 'March', 'April', 'May',
                                                                    'June', 'July', 'August', 'September', 'October',
                                                                    'November', 'December'], dict()
        inner_qs = list(User.objects.values_list('username', flat=True)) if type_user == 'Все' \
            else list(User.objects.filter(groups__name=type_user).values_list('username', flat=True))
        visits = MainStatistics.objects.filter(user__in=inner_qs, dactivity__year=input_year)
        for elem in visits.values('user').order_by().distinct():
            users.append(elem['user'])
        for param in users:
            y_tmp = [0] * len(response['labels'])
            groups = visits.filter(user=param).annotate(
                month=TruncMonth('dactivity')).values('month').annotate(visits=Count('id')).order_by()
            for elem in groups:
                for data in response['labels']:
                    if localtime(elem['month']).strftime('%B') == data:
                        y_tmp[response['labels'].index(data)] = elem['visits']
            response['dict_stacked'][param] = y_tmp, Profile.objects.get(user__username=param).color

    if request.GET['select_type_date'] == 'year':
        colors, i, inner_qs = Dcolors.objects.all().values_list('color', flat=True), 0, \
                              list(User.objects.values_list('username', flat=True)) if type_user == 'Все' \
                                  else list(User.objects.filter(groups__name=type_user).values_list('username',
                                                                                                    flat=True))

        for elem in MainStatistics.objects.filter(user__in=inner_qs).annotate(year=TruncYear('dactivity')).\
                values('year').annotate(count=Count('id')).order_by():
            response[elem['year'].strftime('%Y')] = elem['count'], colors[i]
            i += 1

    return JsonResponse(response)
