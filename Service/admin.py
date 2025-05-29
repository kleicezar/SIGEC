from django.contrib import admin
from .models import *

@admin.register(service)
class serviceAdmin(admin.ModelAdmin):
    list_display = ('id','name_service','is_Active','value_service')
    list_filter = ('name_service','is_Active','value_service')
    search_fields = ('name_service','is_Active','value_service')
    # list_per_page = 10

@admin.register(Vendaservice)
class VendaserviceAdmin(admin.ModelAdmin):
    list_display = ('id','pessoa','data_da_venda','total_value','service_total','discount_total','is_active')
    list_filter = ('pessoa','data_da_venda','total_value','service_total','discount_total','is_active')
    search_fields = ('pessoa','data_da_venda','total_value','service_total','discount_total','is_active')
    # list_per_page = 10
    
@admin.register(VendaItemservice)
class VendaItemserviceAdmin(admin.ModelAdmin):
    list_display = ('id','venda','service','preco','discount')
    list_filter = ('venda','service','preco','discount')
    search_fields = ('venda','service','preco','discount')
    # list_per_page = 10
    
@admin.register(PaymentMethod_Vendaservice)
class PaymentMethod_VendaserviceAdmin(admin.ModelAdmin):
    list_display = ('id','venda','forma_pagamento','expirationDate','valor')
    list_filter = ('venda','forma_pagamento','expirationDate','valor')
    search_fields = ('venda','forma_pagamento','expirationDate','valor')
    # list_per_page = 10



# Register your models here.
