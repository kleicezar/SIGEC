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
from datetime import datetime
import os
import json
import glob

def create_log(msg,date_time):
    now = datetime.now()
    year = now.year
    month = now.month

    # Define o semestre
    semestre = 'S1' if month <= 6 else 'S2'

    # Define diretório e nome fixo do arquivo baseado no semestre
    dir = os.path.join('login', 'log', 'log_entrada')
    os.makedirs(dir, exist_ok=True)
    name_arq = f"log_{year}_{semestre}.json"
    caminho_completo = os.path.join(dir, name_arq)
    if not os.path.exists(caminho_completo):
        with open(caminho_completo, "w") as f:
            f.write(f"Arquivo criado em {date_time}\n")

    if os.path.exists(caminho_completo):
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = {}
    else:
        dados = {}

    # Determina o próximo número de chave
    proximo_id = len(dados) + 1
    chave = f"{proximo_id:010}"  # Ex: "01", "02", etc.

    # Adiciona e salva
    dados[chave] = msg

    with open(caminho_completo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #DADOS PARA ADICIONAR O LOG JSON
            date_time = datetime.now().strftime("%d/%m/%Y as %H:%M:%S")
            msg = f'O Usuario {request.user.username} entrou no sistema no dia {date_time}'
            create_log(msg,date_time)
            return redirect('index')
        
    return render(request, 'login/login.html')

@login_required
def my_logout(request):
    #DADOS PARA ADICIONAR O LOG JSON
    date_time = datetime.now().strftime("%d/%m/%Y as %H:%M:%S")
    msg = f'O Usuario {request.user.username} saiu no sistema no dia {date_time}'
    create_log(msg,date_time)
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

@login_required
def log_entry(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join('login','log','log_entrada', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]

    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)
        print("Último arquivo criado:", os.path.basename(ultimo_arquivo))
    else:
        print("Nenhum arquivo encontrado.")
    caminho_arquivo = os.path.join('login', 'log', 'log_entrada', 'log_2025_S1.json')
    return render(request, 'login/index.html')