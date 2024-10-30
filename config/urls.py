from django.contrib import admin
from django.urls import path, include
from .views import PaymentMethod, PaymentMethodForm

urlpatterns = [
    path('PayMtd/', PaymentMethod, name='PaymentMethod'),
    path('PayMtdform/', PaymentMethodForm, name='PaymentMethodForm')
    ]
