from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('prsn/', client_list, name='Client'),
    path('c/prsn/', Client_Create, name='Client_Create'),
    path('b-prsn/', buscar_clientes, name='buscar_clientes'),
    path('prsn/upt/<int:id_client>/', update_client, name='update_client'),  # Atualizar cliente
    path('prsn/del/<int:id_client>/', delete_client, name='delete_client'),

    # path('tcnch/', Technician_list, name='Technician'),
    # path('c/tcnch/', Technician_Create, name='Technician_Create'),
    # path('b-tcnch/', buscar_Ttchnicianes, name='buscar_Ttchnicianes'),
    # path('tcnch/upt/<int:idtTechnician>/', updatetTechnician, name='updatetTechnician'),  # Atualizar technician
    # path('tcnch/del/<int:idtTechnician>/', deletetTechnician, name='deletetTechnician'),

    # path('Spl/', supplier, name='Supplier'),
    # path('SplForm/', supplierForm, name='SupplierForm'),
    # path('Spl/upt/<int:id_supplier>/', updateSupplier, name='updateSupplier'),
    # path('Spl/dlt/<int:id_supplier>/', deleteSupplier, name='deleteSupplier'),
    ]
