from django.contrib import admin
from django.urls import path, include
from .views import index, PaymentMethod, PaymentMethodForm, Position, PositionForm, Situation, SituationForm

urlpatterns = [
    path('', index, name='index'),
    path('PayMtd/', PaymentMethod, name='PaymentMethod'),
    path('PayMtdform/', PaymentMethodForm, name='PaymentMethodForm'),
    path('Pst/', Position, name='Position'),
    path('PstForm/', PositionForm, name='PositionForm'),
    path('Stn/', Situation, name='Situation'),
    path('StnForm/', SituationForm, name='SituationForm'),
    ]
