from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin , auth

urlpatterns  = [
    path('', views.Expertizi , name='Expertizi'),
    path('ex/', views.Expertizi , name='Expertizi'),
    path('raz/', views.Razreshenie , name='Razreshenie'),
    path('arch/', views.Archive , name='Archive'),
    path('accounts/', include('django.contrib.auth.urls') , name='account'),
    # path('login/', views.LoginFormView.as_view() , name='Login'),
    path('get_table_razreshenie_data/', views.get_table_razreshenie_data , name='get_table_razreshenie_data'),
    path('get_modal_table_razresheniya/', views.get_modal_table_razresheniya , name='get_modal_table_razresheniya'),

    path('get_table_expertizi_data/', views.get_table_expertizi_data, name="get_table_expertizi_data"),
    path('get_table_archive_data/', views.get_table_archive_data, name="get_table_archive_data"),
    path('get_inform_block_ex/', views.get_inform_block_ex, name="get_inform_block_ex"),
    path('get_modal_table_archive/', views.get_modal_table_archive, name="get_modal_table_archive"),

    # path('get_modal_table_new_razresheniya/', views.get_modal_table_new_razresheniya, name="get_modal_table_new_razresheniya"),
    # path('get_modal_info_razresheniya_srok/', views.get_modal_info_razresheniya_srok, name="get_modal_info_razresheniya_srok"),
    #path('get_filter_main_rasreshenie/', views.get_filter_main_rasreshenie, name="get_filter_main_rasreshenie"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)