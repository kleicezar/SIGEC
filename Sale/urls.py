from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('venda/', venda_list, name='venda_list'),
    path('venda/create/', venda_create, name='venda_create'),
    path('venda/update/<int:pk>/', venda_update, name='venda_update'),
    path('venda/delete/<int:pk>/', venda_delete, name='venda_delete'),
    path('venda/<int:venda_pk>/item/create/', venda_item_create, name='venda_item_create'),
    path('venda/buscar_vendas/',buscar_vendas,name='buscar_vendas'),
    path('buscar_pessoas/', client_search, name='buscar_pessoas'),
    path('buscar_fornecedores/',supplier_search,name='buscar_fornecedores'),
    path('buscar_produtos/',product_search,name='buscar_produtos'),
    path('get_product_id/',get_product_id,name='buscar_idprodutos'),
    path('venda/<int:venda_pk>/print', printsale, name='printsale'),
    ]

 