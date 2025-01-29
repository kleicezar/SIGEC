from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('acctpay/', Accounts_list, name='AccountsPayable'),
    path('c/acctpay/', Accounts_Create, name='Accounts_Create'),
    # path('b-acctpay/', buscar_Accounts, name='buscar_Accounts'),
    # path('acctpay/upt/<int:id_Accounts>/', update_Accounts, name='update_Accounts'),  # Atualizar cliente
    # path('acctpay/del/<int:id_Accounts>/', delete_Accounts, name='delete_Accounts'),
    # path('acctpay/get/<int:id_Accounts>/', get_Accounts, name='get_Accounts'),

    path('acctrec/', AccountsReceivable_list, name='AccountsReceivable'),
    path('c/acctrec/', AccountsReceivable_Create, name='AccountsReceivable_Create'),
    # path('b-acctrec/', buscar_AccountsReceivable, name='buscar_AccountsReceivable'),
    # path('acctrec/upt/<int:id_AccountsReceivable>/', update_AccountsReceivable, name='update_AccountsReceivable'),  # Atualizar cliente
    # path('acctrec/del/<int:id_AccountsReceivable>/', delete_AccountsReceivable, name='delete_AccountsReceivable'),
    # path('acctrec/get/<int:id_AccountsReceivable>/', get_AccountsReceivable, name='get_AccountsReceivable'),

    path('b-tech/', search_tech, name='buscar_tech'),
]