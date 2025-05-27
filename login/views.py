from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from finance.models import Accounts, PaymentMethod_Accounts
from .forms import *
from .models import *

def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login/login.html')

@login_required
def my_logout(request):
    logout(request)
    return redirect('index') 
from datetime import date, timedelta
@login_required
def notifications(request):
    today = date.today()
    results = []
    # print("DIA ATUAL: ",today)
    
    for i in range(0,365):
        target_date = today + timedelta(days=i)
        # print(target_date)
        pagamentos = PaymentMethod_Accounts.objects.filter(expirationDate=target_date)
        for pagamento in pagamentos:
            results.append({
                'date':target_date,
                'remainsDays':i,
                'idPayment':pagamento.id
            })
    return JsonResponse({'notifications':results})
@login_required
def index(request):
    return render(request, 'login/index.html')