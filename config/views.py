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
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from .forms import PermissionMultipleSelectForm
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # Para segurança


### PAYMENT METHOD
@login_required
def paymentMethod(request):
    context = {
        'PaymentMethods': PaymentMethod.objects.filter(is_Active=True)
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required
@transaction.atomic
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
            messages.success(request, "Forma de Pagamento cadastrada com sucesso.",extra_tags="successPayment")
            return redirect(previous_url)
    context = {
        'paymentMethod' : paymentMethodForm
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required  
@transaction.atomic  
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
            messages.success(request, "Forma de Pagamento atualizada com sucesso.",extra_tags="successPayment")
            return redirect('PaymentMethod')
    context = {
        'PaymentMethod' : paymentMethodForm
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required
@transaction.atomic
def deletePaymentMethod(request, id_paymentMethod):
    paymentMethod = get_object_or_404(PaymentMethod, id=id_paymentMethod)
    if request.method == "POST":
        paymentMethod.is_Active = False
        paymentMethod.save()
        messages.success(request, "Forma de Pagamento deletada com sucesso.",extra_tags="successPayment")
        return redirect('PaymentMethod')  
    context = {
        'paymentMethod': paymentMethod
    }

    return render(request, 'config/PaymentMethod.html', context)

### POSITION
@login_required
def position(request):
    context = {
        'Positions': Position.objects.filter(is_Active=True)
    }
    return render(request, 'config/Position.html', context)


@login_required
@transaction.atomic
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
            messages.success(request, "Cargo cadastrado com sucesso.",extra_tags='successPosition')
            return redirect('Position')
    context = {
        'Position' : PositionForm
    }
    return render(request, 'config/Position.html', context)

@login_required
@transaction.atomic
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
            messages.success(request, "Cargo atualizado com sucesso.",extra_tags='successPosition')
            return redirect('Position')
    context = {
        'Position' : positionForm
    }
    return render(request, 'config/Position.html', context)

@login_required
@transaction.atomic
def deletePosition(request, id_position):
    position = get_object_or_404(Position, id=id_position)
    if request.method == "POST":
        position.is_Active = False
        position.save()
        messages.success(request, "Cargo deletado com sucesso.",extra_tags="successPosition")
        return redirect('Position')  
    context = {
        'position': position
    }

    return render(request, 'config/Position.html', context)

### SITUATION

@login_required
def situation(request):
    context = {
        'Situations': Situation.objects.filter(is_Active=True)
    }
    return render(request, 'config/Situation.html', context)

@login_required
@transaction.atomic
def SituationForm(request):
    if request.method == "GET":
        situationForm = SituationModelForm()

        v_situation=['V_pessoa' ,'V_data_da_venda' ,'V_total_value' ,'V_discount_total','V_value_apply_credit','V_product' , 'V_quantidade', 'V_preco_unitario', 'V_discount', 'V_price_total', 'V_status', 'V_apply_credit', 'V_product_total', 'V_forma_pagamento', 'V_expirationDate', 'V_valor', 'V_observacao_pessoas', 'V_observacao_sistema', 'V_estagio_inicial', 'V_movement_storage', 'V_movement_accounts']
        os_situation=['OS_pessoa', 'OS_apply_credit', 'OS_data_da_venda', 'OS_observacao_pessoas','OS_observacao_sistema','OS_total_value','OS_product_total','OS_discount_total','OS_value_apply_credit','OS_service_total','OS_discount_total_service','OS_total_value_service','OS_preco','OS_discount','OS_technician','OS_expirationDate','OS_valor','OS_quantidade','OS_preco_unitario','OS_discount','OS_price_total','OS_status','OS_estagio_inicial', 'OS_movement_storage', 'OS_movement_accounts']
        c_situation=['C_fornecedor','C_description','C_product_code','C_barcode','C_unit_of_measure','C_brand','C_cost_of_product','C_selling_price','C_ncm','C_csosn','C_cfop','C_current_quantity','C_maximum_quantity','C_minimum_quantity','C_data_da_compra','C_total_value','C_product_total','C_discount_total','C_observation_product','C_freight_type','C_valueFreight','C_numberOfInstallmentsFreight','C_observation_freight','C_valueTax','C_numberOfInstallmentsTax','C_observation_tax','C_valuePickingList','C_numberOfInstallmentsRMN','C_observation_picking_list','C_quantidade','C_preco_unitario','C_discount','C_price_total','C_estagio_inicial', 'C_movement_storage', 'C_movement_accounts']
        acc_situation=['ACC_description','ACC_pessoa_id', 'ACC_chartOfAccounts','ACC_documentNumber','ACC_date_account', 'ACC_numberOfInstallments','ACC_installment_Range',  'ACC_date_init', 'ACC_totalValue','ACC_peopleWatching','ACC_systemWatching','ACC_plannedAccount','ACC_venda', 'ACC_compra', 'ACC_ordem_servico', 'ACC_forma_pagamento','ACC_expirationDate','ACC_days','ACC_value_old','ACC_value', 'ACC_interestType','ACC_interest', 'ACC_fineType','ACC_fine', 'ACC_acc',  'ACC_activeCredit', 'ACC_paymentPurpose', 'ACC_estagio_inicial', 'ACC_movement_storage', 'ACC_movement_accounts']



        situation_perms = PermsForm()
        context = {
            'form': situationForm,
            'v_situation': v_situation,
            'os_situation': os_situation, 
            'c_situation': c_situation,
            'acc_situation': acc_situation,
        }
        return render(request, 'config/SituationForm.html', context)
    else:
        situationForm = SituationModelForm(request.POST)
        if situationForm.is_valid():
            situationForm.save()
            messages.success(request, "Situação cadastrada com sucesso.",extra_tags='sucessSituation')
            return redirect('Situation')
    context = {
        'form': situationForm,
        'v_situation': v_situation,
    }
    return render(request, 'config/Situation.html', context)

@login_required
@transaction.atomic
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
            messages.success(request, "Situação atualizada com sucesso.",extra_tags='sucessSituation')
            return redirect('Situation')
    context = {
        'Situation' : situationForm
    }
    return render(request, 'config/Situation.html', context)

@login_required
@transaction.atomic
def deleteSituation(request, id_situation):
    situation = get_object_or_404(Situation, id=id_situation)
    if request.method == "POST":
        situation.is_Active = False
        situation.save()
        messages.success(request, "Situação deletada com sucesso.",extra_tags='sucessSituation')
        return redirect('Situation')  # Redirecione para onde desejar
    context = {
        'situation': situation
    }

    return render(request, 'config/Situation.html', context)

### ChartOfAccounts

@login_required
def chartOfAccounts(request):
    context = {
        # 'ChartOfAccounts': ChartOfAccounts.objects.filter(is_Active=True)
        'ChartOfAccounts': ChartOfAccounts.objects.all()
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
@transaction.atomic
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
            messages.success(request, "Plano de Contas cadastrado com sucesso.",extra_tags='successChartOfAccounts')
            return redirect('ChartofAccounts')
        else:
            print('Erros:',chartOfAccountsForm.errors)
    context = {
        'ChartOfAccounts' : chartOfAccountsForm
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
@transaction.atomic
def updateChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "POST":
        chartOfAccountsForm = ChartOfAccountsModelForm(request.POST, instance=chartOfAccounts)
        if chartOfAccountsForm.is_valid():
            chartOfAccounts.code = ''
            chartOfAccountsForm.save()
            messages.success(request, "Plano de Contas atualizado com sucesso.",extra_tags='successChartOfAccounts')
            return redirect('ChartofAccounts')
    elif request.method == "GET":
        chartOfAccountsForm = ChartOfAccountsModelForm(instance=chartOfAccounts)

        context = {
            'ChartOfAccounts': chartOfAccountsForm
        }
        return render(request, 'config/ChartOfAccountsForm.html',context)
    context = {
        'ChartOfAccounts' : chartOfAccountsForm
    }
    return render(request,'config/ChartOfAccounts.html', context)

@login_required
@transaction.atomic
def disableChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "POST":
        chartOfAccounts.is_Active = False
        chartOfAccounts.save()
        messages.success(request, "Plano de Contas desativado com sucesso.",extra_tags='successChartOfAccounts')
        return redirect('ChartofAccounts') 
    context = {
        'chartOfAccounts': chartOfAccounts
    }

    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
@transaction.atomic
def ActiveChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "POST":
        chartOfAccounts.is_Active = True
        chartOfAccounts.save()
        messages.success(request, "Plano de Contas ativado com sucesso.",extra_tags='successChartOfAccounts')
        return redirect('ChartofAccounts')  
    context = {
        'chartOfAccounts': chartOfAccounts
    }

    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
def service(request):
    context = {
        'services':Service.objects.all()
    }
    return render(request,'config/Service.html',context)
    # return HttpResponse("Olá, esta é a minha nova app Django!")

@login_required
@transaction.atomic
def serviceForm(request):
    if request.method == 'POST':
        service_form = serviceModelForm(request.POST)
        print(f'\n\n\n{request.POST}')
        print(f'\n\n\n{service_form.is_valid()}')
        if service_form.is_valid():
            service_form.save() 
            messages.success(request, "Tipo de serviço cadastrado com sucesso.",extra_tags='successservice')
            return redirect('service')
        else: 
            return render(request, 'config/ServiceForm.html', {'form': service_form})
    else:
        service_form = serviceModelForm()
        context = {
            'service':service_form
        }
        return render(request,'config/ServiceForm.html',context)
    
@login_required
@transaction.atomic      
def updateservice(request, pk):
    servico = get_object_or_404(Service, pk=pk)

    if request.method == "POST":
        form = serviceModelForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de serviço atualizado com sucesso.")
            return redirect('service')
    else:
        form = serviceModelForm(instance=servico)

    return render(request, 'config/ServiceForm.html', {'service': form})

@login_required
@transaction.atomic
def deleteservice(request,pk):
    servico = get_object_or_404(service, pk=pk)
    if request.method == "POST":
        servico.is_Active = False
        servico.save()
        messages.success(request, "Tipo de serviço deletado com sucesso.",extra_tags='successservice')
        return redirect('config/service')
    context ={
        'service':servico
    }
    return render(request,'config/service',context)

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

@login_required
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

@login_required
def permitions_list(request):
    users = User.objects.exclude(id = request.user.id)
    context = {
        'users': users
    }
    return render(request, 'config/PermitionsList.html', context)

@login_required
def select_permissions(request, id=id):
    # def editperms(request, id=id):
    user = get_object_or_404(User,id=id)
    permitions = Permission.objects.all()
    if (request.method == 'POST'): 
        # Permissões enviadas pelo formulário
        permissoes_ids = request.POST.getlist('permissoes')
        novas_permissoes = Permission.objects.filter(id__in=permissoes_ids)

        # Remove todas as permissões diretas e adiciona as selecionadas
        user.user_permissions.set(novas_permissoes)

        return redirect('permitions_list')  # ou qualquer outra página que desejar

    else: 
        # users = user.get_all_permissions()
        # u = user.get_all_permissions()
        u = permitions
        users = UserPermissionAssignForm(instance=user)
        for i in u:
            print(i)
        print(type(u))

    # user = get_object_or_404(User, id=id)
    
    # if request.method == "POST":
    #     users = PermsForm(request.POST, instance=user)
    #     if users.is_valid():
    #         messages.success(request, f'Permissao do Usuario {user.username} atualizadas com Sucesso')
    #         return redirect('permitions_list')
    # else: 
    #     users = PermsForm(instance=user) 
    #     print(f'permissoes do usuario {user.get_all_permissions()}')
        # print(f'formulario de permissoes {users}')
    context = {
        'users': users,
        'perm': permitions,
    }
    return render(request, 'config/PermitionsForm.html', context) 

def editperms(request, id=id):
    # Organizar permissões por modelo
    user = get_object_or_404(User, id=id)
    content_types = ContentType.objects.all().order_by('app_label', 'model')
    grouped_permissions = {}

    # for ct in content_types:
    #     perms = Permission.objects.filter(content_type=ct)
    #     if perms.exists():
    #         grouped_permissions[ct] = perms

    if request.method == 'POST':
        form = PermissionMultipleSelectForm(request.POST)
        if form.is_valid():
            selected_perms = form.cleaned_data['permissions']
            user.user_permissions.set(selected_perms)
            return redirect('permitions_list')#, {'perms': selected_perms}
    else:
        print(user.user_permissions.all())
        form = PermissionMultipleSelectForm(initial={'permissions': user.user_permissions.all()})

    return render(request, 'config/PermitionsForm.html', {
        'form': form,
        'grouped_permissions': grouped_permissions
    })

### TESTE

# View para listar os MetaGroups (Supergrupos)
class SuperGroupListView(LoginRequiredMixin, ListView): # Adicionado LoginRequiredMixin
    model = SuperGroup
    template_name = 'sua_app/metagroup_list.html' # Seu template para listar
    context_object_name = 'metagroups'
    # paginate_by = 10 # Opcional: para paginação

# View para criar um novo SuperGroup
class SuperGroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView): # Adicionado Mixins de segurança
    model = SuperGroup
    form_class = SuperGroupForm
    template_name = 'sua_app/metagroup_form.html' # Seu template para o formulário
    success_url = reverse_lazy('sua_app:metagroup_list') # URL para redirecionar após sucesso
    permission_required = 'sua_app.add_metagroup' # Permissão necessária

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Criar Novo Supergrupo'
        return context

# View para editar um SuperGroup existente
class SuperGroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView): # Adicionado Mixins de segurança
    model = SuperGroup # Django pega o 'pk' da URL automaticamente
    form_class = SuperGroupForm
    template_name = 'sua_app/metagroup_form.html'
    success_url = reverse_lazy('sua_app:metagroup_list')
    permission_required = 'sua_app.change_metagroup'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Editar Supergrupo: {self.object.name}'
        return context
    
@login_required
def bank(request):
    context = {
        'Banks': Bank.objects.filter(is_Active=True)
    }
    return render(request, 'config/Bank.html', context)

@login_required
@transaction.atomic
def BankForm(request):
    if request.method == "GET":
        if 'HTTP_REFERER' in request.META:
            request.session['previous_page'] = request.META['HTTP_REFERER']
        bankForm = BankModelForm()
        context = {
            'bank' : bankForm
        }
        return render(request, 'config/BankForm.html', context)
    else:
        bankForm = BankModelForm(request.POST)
         # SALVA O LINK DA PAGINA ANTERIOR
        previous_url = request.session.get('previous_page','/')
        if bankForm.is_valid():

            bankForm.save()
            messages.success(request, "Banco cadastrado com sucesso.",extra_tags="successBank")
            return redirect(previous_url)
    context = {
        'bank' : bankForm
    }
    return render(request, 'config/Bank.html', context)

@login_required  
@transaction.atomic  
def updateBank(request, id_bank):
    bank = get_object_or_404(Bank, id=id_bank)
    if request.method == "GET":
        bankForm = BankModelForm(instance=bank)

        context = {
            'Bank': bank,
            'bank': bankForm
        }
        return render(request, 'config/BankForm.html',context)
    elif request.method == "POST":
        bankForm = BankModelForm(request.POST, instance=bank)
        if bankForm.is_valid():
            bankForm.save()
            messages.success(request, "Forma de Pagamento atualizada com sucesso.",extra_tags="successPayment")
            return redirect('Bank')
    context = {
        'Bank' : bankForm
    }
    return render(request, 'config/Bank.html', context)

@login_required
@transaction.atomic
def deleteBank(request, id_bank):
    bank = get_object_or_404(Bank, id=id_bank)
    if request.method == "POST":
        bank.is_Active = False
        bank.save()
        messages.success(request, "Forma de Pagamento deletada com sucesso.",extra_tags="successPayment")
        return redirect('Bank')  
    context = {
        'bank': bank
    }

    return render(request, 'config/Bank.html', context)
