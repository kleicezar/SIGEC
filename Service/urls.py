from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('wo/create/',workOrders_create,name='workOrdersForm'),
    path('wo/update/<int:pk>/',workOrders_update,name='workOrdersUpdate'),
    path('wo/delete/<int:pk>/',workOrders_delete,name='workOrdersDelete'),
    path('wo/',workOrder,name='workOrders_list'),
    
    path('buscar_servicos/',service_search,name='buscar_servicos'),
    path('get_service_id/',get_service_id,name='get_service_id')
]