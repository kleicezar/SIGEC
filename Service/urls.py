from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('service/', service, name='service_list'),
    path('os/create/',workerService_create,name='orderServiceForm'),
    path('service/create/',service_create,name='serviceForm'),
    path('service/delete/<int:pk>/',delete_service,name='deleteService'),
    path('service/update/<int:pk>/',service_update,name='updateService'),
    path('os/update/<int:pk>/',workerService_update,name='orderServiceUpdate'),
    path('buscar_servicos/',service_search,name='buscar_servicos'),
    path('get_service_id/',get_service_id,name='get_service_id')
]