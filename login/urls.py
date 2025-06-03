from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', my_login, name='login'),
    path('logout/', my_logout, name='logout'),
    path('notifications/',notifications,name='notifications'),
    path('', index, name='index'),
    path('log_entry/', log_entry, name='log_entry'),
    path('log_purchase/', log_purchase, name='log_purchase'),
    path('log_sale/', log_sale, name='log_sale'),
    path('log_service/', log_service, name='log_service'),
    path('log_accounts/', log_accounts, name='log_accounts'),
    path('log_config/', log_config, name='log_config'),
    path('log_permitions/', log_permitions, name='log_permitions'),
    path('log_dlog/', log_dlog, name='log_dlog'),
    ]
