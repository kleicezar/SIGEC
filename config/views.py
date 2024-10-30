from django.shortcuts import render

def index(request):
    return render(request, 'config/index.html')

def PaymentMethod(request):
    return render(request, 'config/PaymentMethod.html')

def PaymentMethodForm(request):
    pass