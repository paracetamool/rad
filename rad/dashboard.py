"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'isov.dashboard.CustomIndexDashboard'
"""

from django.contrib.auth.models import Group
from profiles.models import Dorg
from django.contrib.auth import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class UsersActivity(modules.DashboardModule):
    def is_empty(self):
        pass

    def __init__(self, **kwargs):
        super(UsersActivity, self).__init__(**kwargs)
        self.template = 'grappelli/users_activity.html'
        self.org = kwargs.get('org')


class TrafficGraphs(modules.DashboardModule):
    def is_empty(self):
        pass

    def __init__(self, **kwargs):
        super(TrafficGraphs, self).__init__(**kwargs)
        self.template = 'grappelli/traffic.html'
        self.user_type = kwargs.get('user_type',)
        self.charts = kwargs.get('charts',)


class CustomIndexDashboard(Dashboard):
    class Media:
        css = {
            'all': (
                'admin/custom/css/grappeli-prevent.css',
                'font-awesome-4.7.0/css/font-awesome.min.css',
                'bootstrap-3.3.7/css/bootstrap.min.css',
                'bootstrap-3.3.7/css/bootstrap-theme.min.css',
                'bootstrap-select-1.13.9/css/bootstrap-select.min.css',
                'bootstrap-datetimepicker-4.17.47/css/bootstrap-datetimepicker.min.css',
                'DataTables/datatables.min.css',
                'DataTables/Buttons-1.6.1/css/buttons.bootstrap.min.css',
                'admin/custom/css/dashboard.css',
                'css/bootstrap-datetimepicker.css',
            ),
        }
        js = (
            'jQuery/jquery-3.5.1.min.js',
            'bootstrap-select-1.13.9/js/bootstrap-select.min.js',
            'bootstrap-select-1.13.9/js/i18n/defaults-ru_RU.min.js',
            'js/moment-with-locales.min.js',
            'bootstrap-3.3.7/js/bootstrap.min.js',
            'bootstrap-datetimepicker-4.17.47/js/bootstrap-datetimepicker.min.js',
            'Chart.js-2.9.3/Chart.min.js',
            'js/jquery.mask.min.js',
            'DataTables/DataTables-1.10.20/js/jquery.dataTables.min.js',
            'DataTables/DataTables-1.10.20/js/dataTables.bootstrap.min.js',
            'DataTables/Buttons-1.6.1/js/dataTables.buttons.min.js',
            'DataTables/Buttons-1.6.1/js/buttons.bootstrap.min.js',
            'DataTables/JSZip-2.5.0/jszip.min.js',
            'DataTables/pdfmake-0.1.36/pdfmake.min.js',
            'DataTables/pdfmake-0.1.36/vfs_fonts.js',
            'DataTables/Buttons-1.6.1/js/buttons.html5.min.js',
            'DataTables/Buttons-1.6.1/js/buttons.print.min.js',
            'DataTables/Buttons-1.6.1/js/buttons.colVis.min.js',
            'admin/custom/js/script.js',
        )

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.ModelList(
            title='Быстрые ссылки',
            column=1,
            collapsible=True,
            models=('Expertize.models.Cexpertiza',)
        ))

        self.children.append(modules.ModelList(
            title='Администрирование',
            column=1,
            collapsible=True,
            models=('profiles.models.Dorg', 'django.contrib.*')
        ))

        self.children.append(modules.AppList(
            title='Приложения',
            column=1,
            collapsible=True,
            models=('Expertize.models.*',)
        ))        

        self.children.append(UsersActivity(
            title="Пользователи",
            column=2,
            org=Dorg.objects.all(),
        ))

        self.children.append(TrafficGraphs(
            title="Посещаемость",
            column=2,
            user_type=Group.objects.all(),
            charts=[
                {'id': 'hour_day', 'tab': 'По часам дня'},
                {'id': 'day_week', 'tab': 'По дням недели'},
                {'id': 'day_month', 'tab': 'По дням месяца'},
                {'id': 'month_year', 'tab': 'По месяцам года'},
                {'id': 'year', 'tab': 'По годам'},
            ],
        ))
