from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),

    path('Spl/', supplier, name='Supplier'),
    path('SplForm/', supplierForm, name='SupplierForm'),
    path('Spl/upt/<int:id_supplier>/', updateSupplier, name='updateSupplier'),
    path('Spl/dlt/<int:id_supplier>/', deleteSupplier, name='deleteSupplier'),

    path('Sdct/', product, name='Product'),
    path('SdctForm/', productForm, name='ProductForm'),
    path('Sdct/upt/<int:id_product>/', updateProduct, name='updateProduct'),
    path('Sdct/dlt/<int:id_product>/', deleteProduct, name='deleteProduct'),

    # path('users/', users, name='users'),
    # path('usersform/', usersform, name='usersform')
    
    # path('ClT/', client, name='Client'),
    # path('ClTForm/', clientForm, name='ClientForm'),

    # path('PayMtd/upt/<int:id_paymentMethod>/', updatePaymentMethod, name='updatePaymentMethod'),
    # path('PayMtd/dlt/<int:id_paymentMethod>/', deletePaymentMethod, name='deletePaymentMethod'),

    path('PayMtd/', paymentMethod, name='PaymentMethod'),
    path('PayMtdform/', PaymentMethodForm, name='PaymentMethodForm'),
    path('PayMtd/upt/<int:id_paymentMethod>/', updatePaymentMethod, name='updatePaymentMethod'),
    path('PayMtd/dlt/<int:id_paymentMethod>/', deletePaymentMethod, name='deletePaymentMethod'),

    path('Pst/', position, name='Position'),
    path('PstForm/', PositionForm, name='PositionForm'),
    path('Pst/upt/<int:id_position>/', updatePosition, name='updatePosition'),
    path('Pst/dlt/<int:id_position>/', deletePosition, name='deletePosition'),

    path('Stn/', situation, name='Situation'),
    path('Stn/', deleteSituation, name='deleteSituation'),
    path('StnForm/', SituationForm, name='SituationForm'),
    path('Stn/upt/<int:id_situation>/', updateSituation, name='updateSituation'),
    path('Stn/dlt/<int:id_situation>/', deleteSituation, name='deleteSituation'),

    path('clients/', client_list, name='Client'),
    path('create/client/', create_client, name='create_client'),
    path('client/update/<int:id_client>/', update_client, name='update_client'),  # Atualizar cliente
    path('client/delete/<int:id_client>/', delete_client, name='delete_client'),

    path('venda/', venda_list, name='venda_list'),
    path('venda/create/', venda_create, name='venda_create'),
    path('venda/update/<int:pk>/', venda_update, name='venda_update'),
    path('venda/delete/<int:pk>/', venda_delete, name='venda_delete'),
    path('venda/<int:venda_pk>/item/create/', venda_item_create, name='venda_item_create'),

    path('compras/', compras_list, name='compras_list'),
    path('compras/create/', compras_create, name='compras_create'),
    path('compras/update/<int:pk>/', compras_update, name='compras_update'),
    path('compras/delete/<int:pk>/', compras_delete, name='compras_delete'),
    path('compras/<int:compras_pk>/item/create/', compras_item_create, name='compras_item_create'),
    ]
