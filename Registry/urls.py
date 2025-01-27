from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('prsn/', client_list, name='Client'),
    path('c/prsn/', Client_Create, name='Client_Create'),
    path('b-prsn/', buscar_clientes, name='buscar_clientes'),
    path('prsn/upt/<int:id_client>/', update_client, name='update_client'),  # Atualizar cliente
    path('prsn/del/<int:id_client>/', delete_client, name='delete_client'),
    path('prsn/get/<int:id_client>/', get_client, name='get_client'),

    path('b-tech/', search_tech, name='buscar_tech'),
    ]
