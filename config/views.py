from django.shortcuts import render

def PaymentMethod(request):
    return render(request, 'config/PaymentMethod.html')

def PaymentMethodForm(request):
    pass