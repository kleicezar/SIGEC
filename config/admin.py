from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass

@admin.register(ChartOfAccounts)
class ChartOfAccountsAdmin(admin.ModelAdmin):
    pass

@admin.register(Situation)
class SituationAdmin(admin.ModelAdmin):
    pass

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass

@admin.register(SuperGroup)
class MetaGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('groups', 'members') # Melhora a usabilidade para campos ManyToMany
    search_fields = ('name',)