from django.contrib import admin
from .models import *

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('id','pessoa','data_da_venda','total_value','product_total','discount_total','is_active')
    list_filter = ('pessoa','data_da_venda','total_value','product_total','discount_total','is_active')
    search_fields = ('pessoa','data_da_venda','total_value','product_total','discount_total','is_active')
    # list_per_page = 10

@admin.register(VendaItem)
class VendaItemAdmin(admin.ModelAdmin):
    list_display = ('id','venda','product','quantidade','preco_unitario','discount','price_total')
    list_filter = ('venda','product','quantidade','preco_unitario','discount','price_total')
    search_fields = ('venda','product','quantidade','preco_unitario','discount','price_total')
    # list_per_page = 10
    
@admin.register(PaymentMethod_Venda)
class PaymentMethod_VendaAdmin(admin.ModelAdmin):
    list_display = ('id','venda','forma_pagamento','expirationDate','valor')
    list_filter = ('venda','forma_pagamento','expirationDate','valor')
    search_fields = ('venda','forma_pagamento','expirationDate','valor')
    # list_per_page = 10
    


# Register your models here.
