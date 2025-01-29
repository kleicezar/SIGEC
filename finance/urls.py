from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('acctpay/', AccountsPayable_list, name='AccountsPayable'),
    path('c/acctpay/', AccountsPayable_Create, name='AccountsPayable_Create'),
    # path('b-acctpay/', buscar_AccountsPayable, name='buscar_AccountsPayable'),
    # path('acctpay/upt/<int:id_AccountsPayable>/', update_AccountsPayable, name='update_AccountsPayable'),  # Atualizar cliente
    # path('acctpay/del/<int:id_AccountsPayable>/', delete_AccountsPayable, name='delete_AccountsPayable'),
    # path('acctpay/get/<int:id_AccountsPayable>/', get_AccountsPayable, name='get_AccountsPayable'),

    path('acctrec/', AccountsReceivable_list, name='AccountsReceivable'),
    path('c/acctrec/', AccountsReceivable_Create, name='AccountsReceivable_Create'),
    # path('b-acctrec/', buscar_AccountsReceivable, name='buscar_AccountsReceivable'),
    # path('acctrec/upt/<int:id_AccountsReceivable>/', update_AccountsReceivable, name='update_AccountsReceivable'),  # Atualizar cliente
    # path('acctrec/del/<int:id_AccountsReceivable>/', delete_AccountsReceivable, name='delete_AccountsReceivable'),
    # path('acctrec/get/<int:id_AccountsReceivable>/', get_AccountsReceivable, name='get_AccountsReceivable'),

    path('b-tech/', search_tech, name='buscar_tech'),
]