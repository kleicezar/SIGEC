from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('clients/', client_list, name='Client'),
    path('create/client/', create_client, name='create_client'),
    path('client/update/<int:id_client>/', update_client, name='update_client'),  # Atualizar cliente
    path('client/delete/<int:id_client>/', delete_client, name='delete_client'),

    path('Spl/', supplier, name='Supplier'),
    path('SplForm/', supplierForm, name='SupplierForm'),
    path('Spl/upt/<int:id_supplier>/', updateSupplier, name='updateSupplier'),
    path('Spl/dlt/<int:id_supplier>/', deleteSupplier, name='deleteSupplier'),
    ]
