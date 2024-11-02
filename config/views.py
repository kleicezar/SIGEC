from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *

def index(request):
    return render(request, 'config/index.html')

def PaymentMethod(request):
    return render(request, 'config/PaymentMethod.html')

def PaymentMethodForm(request):
    paymentMethodForm = PaymentMethodModelForm(request.POST)
    if request.method == 'POST':
        if paymentMethodForm.is_valid():
            paymentMethodForm.save()
            messages.success(request, "Usuário cadastrado com sucesso")
            return redirect('paymentMethod')
        else:
            messages.error(request, "Erro ao cadastrar usuário")

    context = {
        'paymentMethod' : paymentMethodForm
    }
    return render(request, 'config/PaymentMethodForm.html', context)
    
def Position(request):
    return render(request, 'config/Position.html')

def PositionForm(request):
    positionForm = PositionModelForm(request.POST)
    if request.method == 'POST':
        if positionForm.is_valid():
            positionForm.save()
            messages.success(request, "Usuário cadastrado com sucesso")
            return redirect('position')
        else:
            messages.error(request, "Erro ao cadastrar usuário")

    context = {
        'position' : positionForm
    }
    return render(request, 'config/PositionForm.html', context)

def Situation(request):
    return render(request, 'config/Situation.html')

def SituationForm(request):
    situationForm = SituationModelForm(request.POST)
    if request.method == 'POST':
        if situationForm.is_valid():
            situationForm.save()
            messages.success(request, "Usuário cadastrado com sucesso")
            return redirect('situation')
        else:
            messages.error(request, "Erro ao cadastrar usuário")

    context = {
        'situation' : situationForm
    }
    return render(request, 'config/SituationForm.html', context)