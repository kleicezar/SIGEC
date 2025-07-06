from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('product/', product, name='Product'),
    path('productForm/', productForm, name='ProductForm'),
    path('product/upt/<int:id_product>/', updateProduct, name='updateProduct'),
    path('product/dlt/<int:id_product>/', deleteProduct, name='deleteProduct'),
    path('product/buscar_produtos/',buscar_produtos,name='buscar_produtos'),
    path('compras/', compras_list, name='compras_list'),
    path('compras/create/', compras_create, name='compras_create'),
    path('compras/update/<int:pk>/', compras_update, name='compras_update'),
    path('compras/delete/<int:pk>/', compras_delete, name='compras_delete'),
    path('compras/<int:compras_pk>/item/create/', compras_item_create, name='compras_item_create'),
    path('get_product_id/',get_product_id,name='buscar_idprodutos'),

    path('mng/manage_product_delivery',productsWithStatus_list,name='manageProductDelivery'),
    path('returnProducts_list/',returnProducts_list,name='returnProducts_list'),
    path('return_product/<int:pk>',return_product,name='return_product'),
    path('expedition_product/<int:pk>/',expedition_product,name='expedition_product'),
    path('update_product_quantity/<int:pk>',update_product_quantity,name="update_product_quantity"),
    
    path('tables/', listTables, name='listTables'),
    path('tableForm/', tableForm, name='TableForm'),
    path('table/upt/<int:id_table>/', updateTable, name='updateTable'),
    path('table/dlt/<int:id_table>/', deleteTable, name='deleteTable'),
]