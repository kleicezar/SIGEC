from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('PayMtd/', paymentMethod, name='PaymentMethod'),
    path('PayMtdform/', PaymentMethodForm, name='PaymentMethodForm'),
    path('PayMtd/upt/<int:id_paymentMethod>/', updatePaymentMethod, name='updatePaymentMethod'),
    path('PayMtd/dlt/<int:id_paymentMethod>/', deletePaymentMethod, name='deletePaymentMethod'),
    path('payMtd/buscar_formaPagamento/',buscar_forma_pagamento,name='buscar_formaPagamento'),

    path('Bank/', bank, name='Bank'),
    path('Bankform/', BankForm, name='BankForm'),
    path('Bank/upt/<int:id_bank>/', updateBank, name='updateBank'),
    path('Bank/dlt/<int:id_bank>/', deleteBank, name='deleteBank'),

    path('Pst/', position, name='Position'),
    path('PstForm/', PositionForm, name='PositionForm'),
    path('Pst/upt/<int:id_position>/', updatePosition, name='updatePosition'),
    path('Pst/dlt/<int:id_position>/', deletePosition, name='deletePosition'),


    path('Stn/', situation, name='Situation'),
    path('Stn/', deleteSituation, name='deleteSituation'),
    path('StnForm/', SituationForm, name='SituationForm'),
    path('Stn/upt/<int:id_situation>/', updateSituation, name='updateSituation'),
    path('Stn/dlt/<int:id_situation>/', deleteSituation, name='deleteSituation'),
    path('Stn/buscar_situacao/',buscar_situacao,name='buscar_situacao'),


    path('chartAcc/',chartOfAccounts,name='ChartofAccounts'),
    path('chartAccForm/',ChartOfAccountsForm,name='ChartOfAccountsForm'),
    path('chartAcc/upt/<int:id_chartOfAccounts>/',updateChartOfAccounts,name='updateChartOfAccounts'),
    path('chartAcc/dlt/<int:id_chartOfAccounts>/',disableChartOfAccounts,name='disableChartOfAccounts'),
    path('chartAcc/act/<int:id_chartOfAccounts>/',ActiveChartOfAccounts,name='ActiveChartOfAccounts'),
    
    path('service/', service, name='service'),
    path('service/create/',serviceForm,name='serviceForm'),
    path('service/delete/<int:pk>/',deleteservice,name='deleteservice'),
    path('service/update/<int:pk>/',updateservice,name='updateservice'),

    path('teste_permissao/', teste_permissao, name='teste_permissao'),

    # path('editperms/<int:id>/', editperms, name='editperms'),
    path('permslist/', permitions_list, name='permitions_list'),

    ###teste
    path('supergrupos/', SuperGroupListView.as_view(), name='metagroup_list'),
    path('supergrupos/novo/', SuperGroupCreateView.as_view(), name='metagroup_create'),
    path('supergrupos/<int:pk>/editar/', SuperGroupUpdateView.as_view(), name='metagroup_update'),

    ]
