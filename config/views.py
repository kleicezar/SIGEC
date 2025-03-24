from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.models import Permission

### PAYMENT METHOD
@login_required
def paymentMethod(request):
    context = {
        'PaymentMethods': PaymentMethod.objects.all()
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required
def PaymentMethodForm(request):
    if request.method == "GET":
        if 'HTTP_REFERER' in request.META:
            request.session['previous_page'] = request.META['HTTP_REFERER']
        paymentMethodForm = PaymentMethodModelForm()
        context = {
            'paymentMethod' : paymentMethodForm
        }
        return render(request, 'config/PaymentMethodForm.html', context)
    else:
        paymentMethodForm = PaymentMethodModelForm(request.POST)
         # SALVA O LINK DA PAGINA ANTERIOR
        previous_url = request.session.get('previous_page','/')
        if paymentMethodForm.is_valid():
            paymentMethodForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect(previous_url)
    context = {
        'paymentMethod' : paymentMethodForm
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required    
def updatePaymentMethod(request, id_paymentMethod):
    paymentMethod = get_object_or_404(PaymentMethod, id=id_paymentMethod)
    if request.method == "GET":
        paymentMethodForm = PaymentMethodModelForm(instance=paymentMethod)

        context = {
            'PaymentMethod': paymentMethod,
            'paymentMethod': paymentMethodForm
        }
        return render(request, 'config/PaymentMethodForm.html',context)
    elif request.method == "POST":
        paymentMethodForm = PaymentMethodModelForm(request.POST, instance=paymentMethod)
        if paymentMethodForm.is_valid():
            paymentMethodForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('PaymentMethod')
    context = {
        'PaymentMethod' : paymentMethodForm
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required
def deletePaymentMethod(request, id_paymentMethod):
    paymentMethod = get_object_or_404(PaymentMethod, id=id_paymentMethod)
    if request.method == "POST":
        paymentMethod.delete()
        messages.success(request, "Situação deletada com sucesso.")
        return redirect('PaymentMethod')  # Redirecione para onde desejar
    context = {
        'paymentMethod': paymentMethod
    }

    return render(request, 'config/PaymentMethod.html', context)

### POSITION
@login_required
def position(request):
    context = {
        'Positions': Position.objects.all()
    }
    return render(request, 'config/Position.html', context)


@login_required
def PositionForm(request):
    if request.method == "GET":
        PositionForm = PositionModelForm()
        context = {
            'Position' : PositionForm
        }
        return render(request, 'config/PositionForm.html', context)
    else:
        PositionForm = PositionModelForm(request.POST)
        if PositionForm.is_valid():
            PositionForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('Position')
    context = {
        'Position' : PositionForm
    }
    return render(request, 'config/Position.html', context)

@login_required
def updatePosition(request, id_position):
    position = get_object_or_404(Position, id=id_position)
    if request.method == "GET":
        positionForm = PositionModelForm(instance=position)

        context = {
            'position': position,
            'Position': positionForm
        }
        return render(request, 'config/PositionForm.html',context)
    elif request.method == "POST":
        positionForm = PositionModelForm(request.POST, instance=position)
        if positionForm.is_valid():
            positionForm.save()
            messages.success(request, "Cargo cadastrado com sucesso")
            return redirect('Position')
    context = {
        'Position' : positionForm
    }
    return render(request, 'config/Position.html', context)

@login_required
def deletePosition(request, id_position):
    position = get_object_or_404(Position, id=id_position)
    if request.method == "POST":
        position.delete()
        messages.success(request, "Situação deletada com sucesso.")
        return redirect('Position')  # Redirecione para onde desejar
    context = {
        'position': position
    }

    return render(request, 'config/Position.html', context)

### SITUATION

@login_required
def situation(request):
  
    context = {
        'Situations': Situation.objects.all()
    }
    return render(request, 'config/Situation.html', context)

@login_required
def SituationForm(request):
    if request.method == "GET":
        situationForm = SituationModelForm()
        context = {
            'Situation' : situationForm
        }
        return render(request, 'config/SituationForm.html', context)
    else:
        situationForm = SituationModelForm(request.POST)
        if situationForm.is_valid():
            situationForm.save()
            messages.success(request, "Situação cadastrada com sucesso")
            return redirect('Situation')
    context = {
        'Situation' : situationForm
    }
    return render(request, 'config/Situation.html', context)

@login_required
def updateSituation(request, id_situation):
    
    situation = get_object_or_404(Situation, id=id_situation)
    if request.method == "GET":
        situationForm = SituationModelForm(instance=situation)

        context = {
            'situation': situation,
            'Situation': situationForm
        }
        return render(request, 'config/SituationForm.html',context)
    elif request.method == "POST":
        situationForm = SituationModelForm(request.POST, instance=situation)
        if situationForm.is_valid():
            situationForm.save()
            messages.success(request, "Situação cadastrada com sucesso")
            return redirect('Situation')
    context = {
        'Situation' : situationForm
    }
    return render(request, 'config/Situation.html', context)

@login_required
def deleteSituation(request, id_situation):
    situation = get_object_or_404(Situation, id=id_situation)
    if request.method == "POST":
        situation.delete()
        messages.success(request, "Situação deletada com sucesso.")
        return redirect('Situation')  # Redirecione para onde desejar
    context = {
        'situation': situation
    }

    return render(request, 'config/Situation.html', context)

### ChartOfAccounts

@login_required
def chartOfAccounts(request):
    context = {
        'ChartOfAccounts': ChartOfAccounts.objects.all()
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
def ChartOfAccountsForm(request):
    if request.method == "GET":
        chartOfAccountsForm = ChartOfAccountsModelForm()
        context = {
            'ChartOfAccounts' : chartOfAccountsForm
        }
        return render(request, 'config/ChartOfAccountsForm.html', context)
    else:
        chartOfAccountsForm = ChartOfAccountsModelForm(request.POST)
        if chartOfAccountsForm.is_valid():
            chartOfAccountsForm.save()
            messages.success(request, "Plano de Contas cadastrado com sucesso")
            return redirect('ChartofAccounts')
        else:
            print('Erros:',chartOfAccountsForm.errors)
    context = {
        'ChartOfAccounts' : chartOfAccountsForm
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
def updateChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "GET":
        chartOfAccountsForm = ChartOfAccountsModelForm(instance=chartOfAccounts)

        context = {
            'chartOfAccounts': chartOfAccounts,
            'ChartOfAccounts': chartOfAccountsForm
        }
        return render(request, 'config/ChartOfAccountsForm.html',context)
    elif request.method == "POST":
        chartOfAccountsForm = ChartOfAccountsModelForm(request.POST, instance=chartOfAccounts)
        if chartOfAccountsForm.is_valid():
            chartOfAccountsForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('ChartofAccounts')
    context = {
        'ChartOfAccounts' : chartOfAccountsForm
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
def deleteChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "POST":
        chartOfAccounts.delete()
        messages.success(request, "Situação deletada com sucesso.")
        return redirect('ChartofAccounts')  # Redirecione para onde desejar
    context = {
        'chartOfAccounts': chartOfAccounts
    }

    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
def service(request):
    print('----------------')
    context = {
        'Services':Service.objects.all()
    }
    return render(request,'config/Service.html',context)
    # return HttpResponse("Olá, esta é a minha nova app Django!")

def ServiceForm(request):
    if request.method == 'POST':
        service_form = ServiceModelForm(request.POST)
        print(f'\n\n\n{request.POST}')
        print(f'\n\n\n{service_form.is_valid()}')
        if service_form.is_valid():
            service_form.save() 
            messages.success(request, "Tipo de Serviço cadastrado com sucesso")
            return redirect('Service')
        else: 
            return render(request, 'config/serviceForm.html', {'form': service_form})
    else:
        service_form = ServiceModelForm()
        context = {
            'service':service_form
        }
        return render(request,'config/serviceForm.html',context)
    
       
def updateService(request,pk):
    servico = get_object_or_404(Service,pk=pk)
    if request.method == "POST":
        service_form = ServiceModelForm(request.POST,instance=servico)
        if service_form.is_valid():
            service_form.save()
            messages.success(request, "Tipo de Serviço atualizado com sucesso")
            # return redirect('orderServiceForm')
            return redirect('Service')

        print(service_form.errors)
    else:
        service_form = ServiceModelForm(instance=servico)
        context = {
            'service':service_form,
        }
        return render(request,'config/serviceForm.html',context)

def deleteService(request,pk):
    servico = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        servico.delete()
        messages.success(request, "Serviço deletada com sucesso.")
        return redirect('config/Service')
    context ={
        'service':servico
    }
    return render(request,'config/Service',context)
@login_required
def buscar_situacao(request):
    query = request.GET.get('query','').strip()
    page_num = request.GET.get('page,1')

    resultados = Situation.objects.filter(
        Q(id__istartswith=query) |
        Q(name_Situation__istartswith=query)
    ).order_by('id')

    situations = [
        {
            'id':situacao.id,
            'name_Situation':situacao.name_Situation,
            'is_Active':situacao.is_Active
        } for situacao in resultados

    ]
    
    usuario_paginator = Paginator(situations,20)
    page = usuario_paginator.get_page(page_num)

    response_data = {
        'situations':list(page.object_list),
        'pagination':{
            'has_previous':page.has_previous(),
            'previous_page':page.previous_page_number() if page.has_previous() else None,
            'has_next':page.has_next(),
            'next_page': page.next_page_number() if page.has_next() else None,
            'current_page': page.number,
            'total_pages': usuario_paginator.num_pages
        },
        'message':f"{len(situations)} Situações encontradas"
    }
    return JsonResponse(response_data)

def buscar_forma_pagamento(request):
    query = request.GET.get('query','').strip()
    page_num = request.GET.get('page,1')

    resultados = PaymentMethod.objects.filter(
        Q(id__istartswith=query)|
        Q(name_paymentMethod__istartswith=query)
    ).order_by('id')

    payments = [
        {
            'id': forma_pagamento.id,
            'name_paymentMethod':forma_pagamento.name_paymentMethod,
            'is_Active':forma_pagamento.is_Active
        } for forma_pagamento in resultados
    ]

    usuario_paginator = Paginator(payments,20)
    page = usuario_paginator.get_page(page_num)

    response_data = {
        'paymentsMethod':list(page.object_list),
        'pagination':{
            'has_previous':page.has_previous(),
            'previous_page':page.previous_page_number() if page.has_previous() else None,
            'has_next':page.has_next(),
            'next_page': page.next_page_number() if page.has_next() else None,
            'current_page': page.number,
            'total_pages': usuario_paginator.num_pages
        },
        'message':f"{len(payments)} Formas de Pagamento encontrados"
    }
    return JsonResponse(response_data)
   
   
@login_required
def teste_permissao(request):
    permissoes = Permission.objects.all()

    permissoes_formatadas = []
    for permissao in permissoes:
        full_codename = f"{permissao.content_type.app_label}.{permissao.codename}"
        tem_permissao = request.user.has_perm(full_codename)  # Verifica na view

        permissoes_formatadas.append({
            "nome": permissao.name,
            "codename": permissao.codename,
            "full_codename": full_codename,
            "tem_permissao": tem_permissao  # Passamos True/False para o template
        })

    return render(request, 'config/testePermissao.html', {"permissoes": permissoes_formatadas})