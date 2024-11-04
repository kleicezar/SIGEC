from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),

    # path('suppliers/', supplier, name='Supplier'),  # Listar todos os fornecedores
    # path('suppliers/new/', supplierForm, name='supplierForm'),  # Criar novo fornecedor
    # path('suppliers/update/<int:id_supplier>/', updateSupplier, name='updateSupplier'),  # Atualizar fornecedor
    # path('suppliers/delete/<int:id>/', deleteSupplier, name='deleteSupplier'),  # Deletar fornecedor

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
    ]
