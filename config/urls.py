from django.contrib import admin
from django.urls import path, include
from .views import index, PaymentMethod, PaymentMethodForm

urlpatterns = [
    path('', index, name='index'),
    path('PayMtd/', PaymentMethod, name='PaymentMethod'),
    path('PayMtdform/', PaymentMethodForm, name='PaymentMethodForm')
    ]
