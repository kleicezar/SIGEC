from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('Sdct/', product, name='Product'),
    path('SdctForm/', productForm, name='ProductForm'),
    path('Sdct/upt/<int:id_product>/', updateProduct, name='updateProduct'),
    path('Sdct/dlt/<int:id_product>/', deleteProduct, name='deleteProduct'),
    path('Sdct/buscar_produtos/',buscar_produtos,name='buscar_produtos'),
    path('compras/', compras_list, name='compras_list'),
    path('compras/create/', compras_create, name='compras_create'),
    path('compras/update/<int:pk>/', compras_update, name='compras_update'),
    path('compras/delete/<int:pk>/', compras_delete, name='compras_delete'),
    path('compras/<int:compras_pk>/item/create/', compras_item_create, name='compras_item_create'),
    path('get_product_id/',get_product_id,name='buscar_idprodutos'),

    path('mng/manage_product_delivery',productsWithStatus_list,name='manageProductDelivery'),
    path('devolutedProduct_list/',devolutedProduct_list,name='devolutedProduct_list'),
    path('devolute_product/<int:pk>',devolute_product,name='devolute_product'),
    path('update_product_quantity/<int:pk>',update_product_quantity,name="update_product_quantity")
]