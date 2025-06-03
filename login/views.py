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
from django.conf import settings
from django.core.paginator import Paginator
import os
import json
import glob

def create_log(msg,date_time,name):
    now = datetime.now()
    year = now.year
    month = now.month

    # Define o semestre
    semestre = 'S1' if month <= 6 else 'S2'

    # Define diretório e nome fixo do arquivo baseado no semestre
    dir = os.path.join('login', 'log', name)
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
    chave = f"{proximo_id}"  # Ex: "01", "02", etc.  "proximo_id:010" deixa 10 digitos no log

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
            create_log(msg,date_time,'log_entrada')
            return redirect('index')
        
    return render(request, 'login/login.html')

@login_required
def my_logout(request):
    #DADOS PARA ADICIONAR O LOG JSON
    date_time = datetime.now().strftime("%d/%m/%Y as %H:%M:%S")
    msg = f'O Usuario {request.user.username} saiu no sistema no dia {date_time}'
    create_log(msg,date_time,'log_entrada')
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
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_entrada', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)
        print("Último arquivo criado:", os.path.basename(ultimo_arquivo))

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)
    else:
        print("Nenhum arquivo encontrado.")

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_purchase(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_compras', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_sale(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_vendas', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_service(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_ordem_de_servico', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_accounts(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_contas', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_config(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_configuracao', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_permitions(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_permissoes', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_dlog(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_de_log', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

def page(request,logs):
    # Converte o dicionário em lista de tuplas
    logs_lista = list(logs.items())  # [('0001', 'desc1'), ('0002', 'desc2'), ...]

    # Cria o paginator — define quantos itens por página (ex.: 10)
    paginator = Paginator(logs_lista, 5)

    # Pega o número da página da URL ?page=2
    page_number = request.GET.get('page')

    # Pega os itens da página atual
    page_obj = paginator.get_page(page_number)
    return page_obj
    