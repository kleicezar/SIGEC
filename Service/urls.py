from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('uepa/', views.index, name='index'),
    path('os/create/',workerService_create,name='orderServiceForm'),
    path('service/create/',service_create,name='serviceForm'),
    path('service/update/<int:pk>/',service_update,name='serviceUpdate'),
    path('os/update/<int:pk>/',workerService_update,name='orderServiceUpdate'),
    path('buscar_servicos/',service_search,name='buscar_servicos'),
    path('get_service_id/',get_service_id,name='get_service_id')
]