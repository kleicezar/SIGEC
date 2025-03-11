from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    pass

@admin.register(CompraItem)
class CompraItemAdmin(admin.ModelAdmin):
    pass




# Register your models here.
