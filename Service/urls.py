from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('os/create/',workerService_create,name='orderServiceForm'),
    path('os/update/<int:pk>/',workerService_update,name='orderServiceUpdate'),
    path('os/delete/<int:pk>/',deleteWorkService,name='deleteWorkService'),
    path('os/',workService,name='OrderService'),
    path('service/', service, name='service_list'),
   
    path('service/create/',service_create,name='serviceForm'),
    path('service/delete/<int:pk>/',delete_service,name='deleteService'),
    path('service/update/<int:pk>/',service_update,name='updateService'),
    path('buscar_servicos/',service_search,name='buscar_servicos'),
    path('get_service_id/',get_service_id,name='get_service_id')
]