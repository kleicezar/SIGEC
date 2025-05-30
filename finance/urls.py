from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('AccountsPayable/', AccountsPayable_list, name='AccountsPayable'),
    path('c/AccountsPayable/', Accounts_Create, name='Accounts_Create'),
    # path('b-AccountsPayable/', buscar_Accounts, name='buscar_Accounts'),
    path('AccountsPayable/upt/<int:id_Accounts>/', update_Accounts, name='update_Accounts'),  # Atualizar cliente
    path('AccountsPayable/del/<int:id_Accounts>/', delete_Accounts, name='delete_Accounts'),
    path('AccountsPayable/get/<int:id_Accounts>/', get_Accounts, name='get_Accounts'),

    path('AccountsReceivable/', AccountsReceivable_list, name='AccountsReceivable'),
    path('c/AccountsReceivable/', AccountsReceivable_Create, name='AccountsReceivable_Create'),
    # path('b-AccountsReceivable/', buscar_AccountsReceivable, name='buscar_AccountsReceivable'),
    path('AccountsReceivable/upt/<int:id_Accounts>/', update_AccountsReceivable, name='update_AccountsReceivable'),  # Atualizar cliente
    path('AccountsReceivable/del/<int:id_Accounts>/', delete_AccountsReceivable, name='delete_AccountsReceivable'),
    path('AccountsReceivable/get/<int:id_Accounts>/', get_AccountsReceivable, name='get_AccountsReceivable'),

    path('credit/upt/<int:id_client>/',Credit_Update,name='update_creditLimit'),

    path('updateReceivableSale/upt/<int:id_Accounts>/',updateAccounts_Sale,name='update_AccountsReceivableAccounts'),

    path('creditedClients/',CreditedClients_list,name='CreditedClients'),
    path('accounts_list/<int:id_accounts>/',Accounts_list,name='Accounts_list'),
    path('delete_payments/<int:id>/',deletePayment_Accounts,name='delete_payments'),
    path('cashFlow/get/', cashFlow, name='cashFlow'),

]