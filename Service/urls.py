from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('uepa/', views.index, name='index'),
    path('os/create/',orderService_create,name='orderServiceForm'),
    path('service/create/',service_create,name='serviceForm')
]