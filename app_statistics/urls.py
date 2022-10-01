from django.urls import include, path
from . import views

urlpatterns = [
    path(r'^get_users_data/$', views.get_users_data, name='get_users_data'),
    path(r'^get_traffic_data/$', views.get_traffic_data, name='get_traffic_data'),
    path(r'^profile_info/(?P<pk>\d+)/$', views.profile_info, name='profile_info'),
]
