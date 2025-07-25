from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from purchase.forms import CompraFormUpdate
from registry.models import Credit
from sale.forms import VendaForm, VendaFormUpdate
from sale.views import venda_update
from service.forms import VendaServiceFormUpdate, VendaserviceForm
from service.views import workOrders_update
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
import pdb
from django.db import transaction

### CONTAS A PAGAR

# funcionando
@login_required
@transaction.atomic 
def Accounts_Create(request):
    dados = request.session.get('dados_temp')
    plannedAccount = request.GET.get("plannedAccount",'false')
    
    print(plannedAccount)
    verify = 0
    installments = []
    # PaymentMethodAccountsFormSet = inlineformset_factory(Accounts, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(
        Accounts,
        PaymentMethod_Accounts,
        form=PaymentMethodAccountsForm,
        extra=1, 
        can_delete=True,
    )
    if request.method == "POST":
        
        post_data = request.POST.copy()
        raw_data_planned_account = post_data.get('plannedAccount')
        if raw_data_planned_account:
            raw_date = post_data.get('date_init')
            if raw_date:
                try:
                    date_obj = datetime.strptime(raw_date,"%m/%Y")
                    completed_date = date_obj.replace(day=1).date()
                    post_data['date_init'] = completed_date.isoformat()
                    form_Accounts = AccountsFormPlannedAccount(post_data)
                except ValueError as e:
                    print("Erro ao tratar date_init",e)
        else:
            form_Accounts = AccountsForm(request.POST)
        
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)
        print(f"Total de formulários no formset: {len(PaymentMethod_Accounts_FormSet)}")
        print(f"Formulários que foram alterados (has_changed): {[form.has_changed() for form in PaymentMethod_Accounts_FormSet]}")
        # raw_date_init = post_data.get('date_init')
        # if raw_date_init:
        #     # Exemplo: garantir que está no formato YYYY-MM-DD
        #     treated_date = raw_date_init.strip()  # aqui você pode usar um parser também
        #     post_data['date_init'] = treated_date

        if form_Accounts.is_valid() and PaymentMethod_Accounts_FormSet.is_valid():

            # FIXME adicionar valor antigo e fazer comparação entre antigo, novo e gerar a parcela de desconto 

            account = form_Accounts.save()
            total_value = account.totalValue

            print(f'\n\nQuantidade de formulários no FormSet: {len(PaymentMethod_Accounts_FormSet)}\n\n')

            for form in PaymentMethod_Accounts_FormSet: 
                print('\npassou pelo if is_valid()\n')
                print(f'formulario unitario: {form}')
                if form.cleaned_data:
                    print('\npassou pelo if cleaned_data()\n')

                    parcela = form.cleaned_data['value']
                    form.cleaned_data['value_old'] = parcela
                    verify += parcela
                    form_cleaned = form.save(commit=False)
                    installments.append(form_cleaned)
                if float(verify) == float(total_value):
                    for installment in installments:
                        installment.conta = account
                        installment.acc = True
                        installment.save()
                    messages.success(request,"Conta criada com sucesso.",extra_tags="successAccount")
                    return redirect('AccountsPayable')
                else:
                    print('\npassou pelo else verify()\n')

                    form.add_error('value', f'O valor do somatorio das parcelas ({parcela}) é inferior ao Valor Total ({total_value}).')
        else:
            # print("Erros no form_Accounts:", form_Accounts.errors)
            # print("Erros no PaymentMethod_Accounts_FormSet:", PaymentMethod_Accounts_FormSet.errors)
            # Aqui, o formset não é válido, vamos imprimir os erros para diagnóstico
            print(f"Erros no formulario de FormAccounts",form_Accounts.errors)
            for form in PaymentMethod_Accounts_FormSet:
                print(f"Erros no formulário {form.instance}: {form.errors}")
            print()
            print("Erros do formset (non_field_errors):", PaymentMethod_Accounts_FormSet.non_form_errors())

            # Opcional: Você pode exibir os erros de cada campo individualmente
            for form in PaymentMethod_Accounts_FormSet:
                for field in form:
                    if field.errors:
                        print(f"Erro no campo {field.name}\t: {field.errors}")
            
            # Retorna para o template com os erros
            context = {
                'form_payment_account': PaymentMethod_Accounts_FormSet, 
                'tipo_conta': 'Receber'
            }
            return render(request, 'finance/AccountsPayform.html', context)
    else: 
        referer = request.META.get('HTTP_REFERER', '')
        if dados and 'return_product' in referer:
            description = dados.get('description')
            person = dados.get('person')
            totalValue = dados.get('totalValue')
            if plannedAccount == 'false':
                initial_data = {
                'description':description,
                'pessoa_id':person,
                'totalValue':totalValue
                }
                form_Accounts = AccountsForm(initial_data)
            else:
                initial_data = {
                'plannedAccount': plannedAccount,
                'description':description,
                'pessoa_id':person,
                'totalValue':totalValue
                }
                form_Accounts = AccountsFormPlannedAccount(initial=initial_data)
            
        else:
            if plannedAccount =='false':
                form_Accounts = AccountsForm()
                # form_Accounts.fields['installment_Range'].choices = Accounts.INSTALLMENT_RANGE_CHOICES
            else:

                initial_data = {
                'plannedAccount': plannedAccount,
                }

                form_Accounts = AccountsFormPlannedAccount(initial=initial_data)
       
            # form_Accounts.fields['installment_Range'].choices = Accounts.INSTALLMENT_RANGE_CHOICES_PLANNED_ACCOUNT
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())

    context = {
        'form_Accounts': form_Accounts,
        'form_payment_account': PaymentMethod_Accounts_FormSet,
        'Contas' : 'Contas a Pagar',
        'tipo_conta': 'Pagar'
    }
    return render(request, 'finance/AccountsPayform.html', context)

# funcionando
@login_required
def AccountsPayable_list(request):
    # Obtenha o termo de pesquisa da requisição
    search_query = request.GET.get('query', '')
 

    # Filtrar os clientes com base no termo de pesquisa
    if search_query:
        account = PaymentMethod_Accounts.objects.filter(
        (   # campo pessoa
           (
                Q(id__icontains=search_query) | 
                Q(conta__pessoa_id__id_FisicPerson_fk__name__icontains=search_query) | 
                Q(conta__pessoa_id__id_LegalPerson_fk__name_foreigner__icontains=search_query) | 
                Q(conta__pessoa_id__id_ForeignPerson_fk__fantasyName__icontains=search_query) | 
                Q(documentNumber__icontains=search_query)
            ) & (Q(compra__is_active = True) | Q(conta__is_active = True))
        ),
        conta__acc = True
       
    ).order_by('id')
    else:
        account = PaymentMethod_Accounts.objects.filter(
            (Q(compra__is_active = True) | Q(conta__is_active = True)),
            acc = True).order_by('id') 

    paginator = Paginator(account, 20)  
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'finance/AccountsPay_list.html', {
        'accounts': page,
        'query': search_query,  # Envie o termo de pesquisa para o template
        'ContasP' : 'Contas a Pagar'
    })

# funcionando
@login_required
def get_Accounts(request, id_Accounts):
    paymentMethod_Accounts = PaymentMethod_Accounts.objects.get(id=id_Accounts,acc=True)
    client = {
    'pessoa_id':paymentMethod_Accounts.conta.pessoa_id,
    'chartOfAccounts': paymentMethod_Accounts.conta.chartOfAccounts,
    'documentNumber':paymentMethod_Accounts.conta.documentNumber,
    'date_account':paymentMethod_Accounts.conta.date_account,
    'numberOfInstallments': paymentMethod_Accounts.conta.numberOfInstallments,
    'installment_Range':paymentMethod_Accounts.conta.installment_Range,
    'date_init':paymentMethod_Accounts.conta.date_init,
    'totalValue':paymentMethod_Accounts.conta.totalValue,
    'peopleWatching':paymentMethod_Accounts.conta.peopleWatching,
    'systemWatching':paymentMethod_Accounts.conta.systemWatching,
    'forma_pagamento':paymentMethod_Accounts.forma_pagamento,
    'expirationDate':paymentMethod_Accounts.expirationDate,
    'value':paymentMethod_Accounts.value,
    'value_old':paymentMethod_Accounts.value_old,
    'interest':paymentMethod_Accounts.interest,
    'fine':paymentMethod_Accounts.fine,
    }
        
    return render(request, 'finance/AccountsPay_GET.html', {'client': client})

@login_required
@transaction.atomic 
def update_Accounts(request, id_Accounts):
    payment_instance = get_object_or_404(PaymentMethod_Accounts, id=id_Accounts)
    if payment_instance.conta:
        accounts_instance = get_object_or_404(Accounts, id=payment_instance.conta_id)
        print('accounts_instance', accounts_instance)
        if request.method == "POST":  
            payment_form_instance = PaymentMethodAccountsForm(request.POST, instance=payment_instance)
            accounts_form_instance = AccountsFormUpdate(
                request.POST, 
                instance=accounts_instance,
                initial={
                    'numberOfInstallments': accounts_instance.numberOfInstallments,
                    'installment_Range': accounts_instance.installment_Range,
                    'totalValue': accounts_instance.totalValue,
                    'date_init': accounts_instance.date_init
                }
            )
            for key, value in vars(payment_instance).items(): 
                print(f"{key}: {value}")
            print()
            # for key, value in vars(accounts_instance).items():
            #     print(f"{key}: {value}")
            # print()

            if payment_form_instance.is_valid() and accounts_form_instance.is_valid():
                accounts_form_instance.save()

                payment_instance = payment_form_instance.save(commit=False)

                # Definir None para valores vazios
                if not payment_instance.interest:
                    payment_instance.interest = None
                if not payment_instance.fine:
                    payment_instance.fine = None

                payment_instance.acc = True
                payment_instance.save()
                messages.success(request,"Conta atualizada com sucesso.",extra_tags="successAccount")
                return redirect('AccountsPayable')  # Redirecionar após salvar
            else:
                print("Erros no payment_form_instance:", payment_form_instance.errors)
                print()
                print("Erros no accounts_form_instance:", accounts_form_instance.errors)
                print()


        else:
            accounts_form_instance = AccountsFormUpdate(instance=accounts_instance)
            payment_form_instance = PaymentMethodAccountsFormUpdate(instance=payment_instance)

        context = {
            'form_Accounts': accounts_form_instance,
            'form_paymentMethodAccounts': payment_form_instance,
            'tipo_conta': 'Receber'
        }

        return render(request, 'finance/AccountsPayformUpdate.html', context)
    else:
        if payment_instance.compra:
            return updateAccounts_Shopping(request,payment_instance.id)

@login_required
@transaction.atomic 
def updateAccounts_Shopping(request,id_Accounts):
    payment_instance = get_object_or_404(PaymentMethod_Accounts, id=id_Accounts)
    if request.method == "POST":
        payment_form_instance = PaymentMethodAccountsForm(request.POST,instance=payment_instance)

        if payment_instance.compra:
            accounts_instance = get_object_or_404(Compra, id=payment_instance.compra.id)
            accounts_form_instance = CompraFormUpdate(request.POST,instance=accounts_instance)
            
        if payment_form_instance.is_valid() and accounts_form_instance.is_valid():
            accounts_form_instance.save()

            payment_instance = payment_form_instance.save(commit=False)

            if not payment_instance.interest:
                payment_instance.interest = None
            if not payment_instance.fine:
                payment_instance.fine = None
            payment_instance.acc = True
            payment_instance.save()
            messages.success(request,"Conta atualizada com sucesso.",extra_tags="successAccount")
            return redirect('AccountsPayable') 
        
        if not payment_form_instance.is_valid():
            print('irra')
        if not accounts_form_instance.is_valid():
            print('Erros na Conta a Pagar',accounts_form_instance.errors)
        
    else:
        if payment_instance.compra:
            id = payment_instance.compra.id
            accounts_instance = get_object_or_404(Compra, id=id)
            accounts_form_instance = CompraFormUpdate(instance=accounts_instance)

        payment_form_instance = PaymentMethodAccountsFormUpdate(instance=payment_instance)
    
    context = {
        'form_Accounts':accounts_form_instance,
        'form_paymentMethodAccounts':payment_form_instance,
        'tipo_conta':'Pagar'
    }
    return render(request, 'finance/AccountsPayformShoppingUpdate.html', context)

@login_required
@transaction.atomic 
def updateAccounts_Sale(request,id_Accounts):
    print("passei")
    payment_instance = get_object_or_404(PaymentMethod_Accounts, id=id_Accounts)

    if request.method == "POST":
        print('DADOS DO REQUEST.POST',request.POST)
        payment_form_instance = PaymentMethodAccountsForm(request.POST,instance=payment_instance)
        if payment_instance.venda:
            accounts_instance = get_object_or_404(Venda, id=payment_instance.venda.id)
            accounts_form_instance = VendaFormUpdate(request.POST,instance=accounts_instance)
        
        if payment_instance.ordem_servico:
            accounts_instance =  get_object_or_404(Vendaservice, id=payment_instance.ordem_servico.id)
            accounts_form_instance = VendaServiceFormUpdate(request.POST,instance=accounts_instance)
        
        if payment_form_instance.is_valid() and accounts_form_instance.is_valid():
            
            accounts_form_instance.save()

            payment_instance = payment_form_instance.save(commit=False)

            if not payment_instance.interest:
                payment_instance.interest = None
            if not payment_instance.fine:
                payment_instance.fine = None

            payment_instance.save() 
            messages.success(request,"Conta atualizada com sucesso.",extra_tags="successAccount")
            return redirect('AccountsReceivable') 
    else:
        if payment_instance.venda:
            accounts_instance = get_object_or_404(Venda, id=payment_instance.venda.id)
            accounts_form_instance = VendaFormUpdate(instance=accounts_instance)
        
        if payment_instance.ordem_servico:
            accounts_instance =  get_object_or_404(Vendaservice, id=payment_instance.ordem_servico.id)
            accounts_form_instance = VendaServiceFormUpdate(instance=accounts_instance)

        print('accounts_instance', accounts_instance)
        payment_form_instance = PaymentMethodAccountsFormUpdate(instance=payment_instance)
    
    context = {
        'form_Accounts':accounts_form_instance,
        'form_paymentMethodAccounts':payment_form_instance,
        'tipo_conta':'Receber'
    }
    return render(request, 'finance/AccountsPayformSaleUpdate.html', context)

# funcionando
@login_required
@transaction.atomic 
def delete_Accounts(request, id_Accounts):
    # Recupera o accounte com o id fornecido
    account_deleta_pelo_amor_De_Deus = PaymentMethod_Accounts.objects.filter(id=id_Accounts,acc = True).delete()
    messages.success(request,"Conta deletada com sucesso.",extra_tags="successAccount") 
    return redirect('AccountsPayable')

### CONTAS A RECEBER

@login_required
@transaction.atomic 
def AccountsReceivable_Create(request):

    plannedAccount = request.GET.get("plannedAccount",'false')
    verify = 0
    installments = []
    # PaymentMethodAccountsFormSet = inlineformset_factory(Accounts, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(
        Accounts,
        PaymentMethod_Accounts,
        form=PaymentMethodAccountsForm,
        extra=1, 
        can_delete=True,
        
    )
    if request.method == "POST":


        post_data = request.POST.copy()
        raw_data_planned_account = post_data.get('plannedAccount')
        if raw_data_planned_account:
            raw_date = post_data.get('date_init')
            if raw_date:
                try:
                    date_obj = datetime.strptime(raw_date,"%m/%Y")
                    completed_date = date_obj.replace(day=1).date()
                    post_data['date_init'] = completed_date.isoformat()
                    form_Accounts = AccountsFormPlannedAccount(post_data)
                except ValueError as e:
                    print("Erro ao tratar date_init",e)
        else:
            form_Accounts = AccountsForm(request.POST)

        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)

        if form_Accounts.is_valid() and PaymentMethod_Accounts_FormSet.is_valid():

            # FIXME adicionar valor antigo e fazer comparação entre antigo, novo e gerar a parcela de desconto 

            account = form_Accounts.save()
            total_value = account.totalValue

            print(f'\n\nQuantidade de formulários no FormSet: {len(PaymentMethod_Accounts_FormSet)}\n\n')

            for form in PaymentMethod_Accounts_FormSet: 
                if form.cleaned_data:
                    print('\npassou pelo if cleaned_data()\n')

                    parcela = form.cleaned_data['value']
                    form.cleaned_data['value_old'] = parcela
                    verify += parcela
                    form_cleaned = form.save(commit=False)
                    installments.append(form_cleaned)
                if float(verify) == float(total_value):
                    for installment in installments:
                        installment.conta = account
                        installment.acc = False
                        installment.save()
                    messages.success(request,"Conta cadastrada com sucesso.",extra_tags="successAccount")
                    return redirect('AccountsReceivable')
                else:
                    print('\npassou pelo else verify()\n')

                    form.add_error('value', f'O valor do somatorio das parcelas ({parcela}) é inferior ao Valor Total ({total_value}).')
        else:

            print(f"Erros no formulario de FormAccounts",form_Accounts.errors)
            for form in PaymentMethod_Accounts_FormSet:
                print(f"Erros no formulário {form.instance}: {form.errors}")
            print()
            # Opcional: Você pode exibir os erros de cada campo individualmente
            for form in PaymentMethod_Accounts_FormSet:
                for field in form:
                    if field.errors:
                        print(f"Erro no campo {field.name}\t: {field.errors}")
            
            # Retorna para o template com os erros
            context = {
                'form_payment_account': PaymentMethod_Accounts_FormSet, 
                'tipo_conta': 'Receber'
            }
            return render(request, 'finance/AccountsPayform.html', context)
    else: 
        if plannedAccount == 'false':
            form_Accounts = AccountsForm()
        else:
            initial_data = {
            'plannedAccount': plannedAccount,
            }

            form_Accounts = AccountsFormPlannedAccount(initial=initial_data)

        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        
    context = {
        'form_Accounts': form_Accounts,
        'form_payment_account': PaymentMethod_Accounts_FormSet,
        'Contas' : 'Contas a Receber',
        'tipo_conta': 'Receber'
    }

    return render(request, 'finance/AccountsPayform.html', context)

@login_required
def AccountsReceivable_list(request):
    # Obtenha o termo de pesquisa da requisição
    search_query = request.GET.get('query', '') 

    # Filtrar os accountes com base no termo de pesquisa
    if search_query:
        account = PaymentMethod_Accounts.objects.filter(
        (   # campo pessoa
            (
                Q(id__icontains=search_query) | 
                Q(conta__pessoa_id__id_FisicPerson_fk__name__icontains=search_query) | 
                Q(conta__pessoa_id__id_LegalPerson_fk__name_foreigner__icontains=search_query) | 
                Q(conta__pessoa_id__id_ForeignPerson_fk__fantasyName__icontains=search_query) | 
                Q(documentNumber__icontains=search_query)
            ) & (Q(venda__is_active=True) | Q(ordem_servico__is_active=True) | Q(conta__is_active=True))     
        ),
        acc = False 
    ).order_by('id')
    else:
        account = PaymentMethod_Accounts.objects.filter(
            (Q(venda__is_active=True) | Q(ordem_servico__is_active=True) | Q(conta__is_active = True)),
            acc = False).order_by('id') 

    # Configure o Paginator com o queryset filtrado
    paginator = Paginator(account, 20) 
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'finance/AccountsPay_list.html', {
        'accounts': page,
        'query': search_query,  # Envie o termo de pesquisa para o template
        'ContasR' : 'Contas a Receber'

    })

@login_required
def AccountsReceivable_listnovo(request):
    # Obtenha o termo de pesquisa da requisição
    search_query = request.GET.get('query', '') 
    # Filtrar os accountes com base no termo de pesquisa
    if search_query:
        account = PaymentMethod_Accounts.objects.filter(
        (   # campo pessoa
            Q(id__icontains=search_query) | 
            Q(conta__pessoa_id__id_FisicPerson_fk__name__icontains=search_query) | 
            Q(conta__pessoa_id__id_LegalPerson_fk__name_foreigner__icontains=search_query) | 
            Q(conta__pessoa_id__id_ForeignPerson_fk__fantasyName__icontains=search_query) | 
            Q(documentNumber__icontains=search_query)
        ),
        acc = False 
    ).order_by('id')
    else:
        account = PaymentMethod_Accounts.objects.filter(acc = False).order_by('id') 

    # Configure o Paginator com o queryset filtrado
    paginator = Paginator(account, 20) 
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'finance/AccountsPay_listnovo.html', {
        'accounts': page,
        'query': search_query,  # Envie o termo de pesquisa para o template
        'ContasR' : 'Contas a Receber'

    })

# funcionando
@login_required
def get_AccountsReceivable(request, id_Accounts):
    paymentMethod_Accounts = PaymentMethod_Accounts.objects.get(id=id_Accounts,acc=False)
    client = {
    'pessoa_id':paymentMethod_Accounts.conta.pessoa_id,
    'chartOfAccounts': paymentMethod_Accounts.conta.chartOfAccounts,
    'documentNumber':paymentMethod_Accounts.conta.documentNumber,
    'date_account':paymentMethod_Accounts.conta.date_account,
    'numberOfInstallments': paymentMethod_Accounts.conta.numberOfInstallments,
    'installment_Range':paymentMethod_Accounts.conta.installment_Range,
    'date_init':paymentMethod_Accounts.conta.date_init,
    'totalValue':paymentMethod_Accounts.conta.totalValue,
    'peopleWatching':paymentMethod_Accounts.conta.peopleWatching,
    'systemWatching':paymentMethod_Accounts.conta.systemWatching,
    'forma_pagamento':paymentMethod_Accounts.forma_pagamento,
    'expirationDate':paymentMethod_Accounts.expirationDate,
    'value':paymentMethod_Accounts.value,
    'value_old':paymentMethod_Accounts.value_old,
    'interest':paymentMethod_Accounts.interest,
    'fine':paymentMethod_Accounts.fine,
    }
    
        
    return render(request, 'finance/AccountsPay_GET.html', {'client': client})

@login_required
@transaction.atomic 
def update_AccountsReceivable(request, id_Accounts):
    payment_instance = get_object_or_404(PaymentMethod_Accounts, id=id_Accounts)
    if payment_instance.conta:
        accounts_instance = get_object_or_404(Accounts, id=payment_instance.conta_id)
        print('accounts_instance', accounts_instance)
        if request.method == "POST":  
            payment_form_instance = PaymentMethodAccountsForm(request.POST, instance=payment_instance)
            accounts_form_instance = AccountsFormUpdate(
                request.POST, 
                instance=accounts_instance,
                initial={
                    'numberOfInstallments': accounts_instance.numberOfInstallments,
                    'installment_Range': accounts_instance.installment_Range,
                    'totalValue': accounts_instance.totalValue,
                    'date_init': accounts_instance.date_init
                }
            )
            for key, value in vars(payment_instance).items(): 
                print(f"{key}: {value}")
            print()
            # for key, value in vars(accounts_instance).items():
            #     print(f"{key}: {value}")
            # print()

            if payment_form_instance.is_valid() and accounts_form_instance.is_valid():
                accounts_form_instance.save()

                payment_instance = payment_form_instance.save(commit=False)

                # Definir None para valores vazios
                if not payment_instance.interest:
                    payment_instance.interest = None
                if not payment_instance.fine:
                    payment_instance.fine = None


                payment_instance.save()
                messages.success(request,"Conta atualizada com sucesso.",extra_tags="successAccount")
                return redirect('AccountsReceivable')  # Redirecionar após salvar
            else:
                print("Erros no payment_form_instance:", payment_form_instance.errors)
                print()
                print("Erros no accounts_form_instance:", accounts_form_instance.errors)
                print()


        else:
            accounts_form_instance = AccountsFormUpdate(instance=accounts_instance)
            payment_form_instance = PaymentMethodAccountsFormUpdate(instance=payment_instance)

        context = {
            'form_Accounts': accounts_form_instance,
            'form_paymentMethodAccounts': payment_form_instance,
            'tipo_conta': 'Receber'
        }
        return render(request, 'finance/AccountsPayformUpdate.html', context)
    else:
        if payment_instance.venda or payment_instance.ordem_servico:
            return updateAccounts_Sale(request,payment_instance.id)
        # elif payment_instance.ordem_servico:
        #     return workOrders_update(request,payment_instance.ordem_servico.id)
# funcionando

@login_required
@transaction.atomic 
def delete_AccountsReceivable(request, id_Accounts):
    # Recupera o accounte com o id fornecido
    messages.success(request,"Conta deletada com sucesso.",extra_tags="successAccount")
    account_deleta_pelo_amor_De_Deus = PaymentMethod_Accounts.objects.filter(id=id_Accounts,acc = False).delete() #filter(acc = False)
    return redirect('AccountsReceivable')

@login_required
@transaction.atomic 
def Credit_Update(request,id_client):
    person = Person.objects.get(id=id_client)
    if request.method == "POST":
        form_creditLimit = CreditLimitForm(request.POST,instance=person)
        if form_creditLimit.is_valid():
            person.creditLimit = form_creditLimit.cleaned_data["creditLimit"]
            person.save()
            messages.success(request,"Crédito atualizado com sucesso.",extra_tags='successCredit')
            return redirect('CreditedClients')
        else:
            print("Erro no formulário de Limite de Crédito",form_creditLimit.errors)
    else:
        form_creditLimit = CreditLimitForm(instance=person)

        context = {
            'form_creditLimit':form_creditLimit
        }
    return render(request,'finance/Creditform.html',context)

@login_required
@transaction.atomic 
def CreditedClients_list(request):
    
    persons = Person.objects.all()
    return render(request,"finance/CreditedClients.html",{'persons':persons})

@login_required
@transaction.atomic 
def Credit_list(request):
    credits = Credit.objects.all()
    colunas = [
        ('id','ID'),
        ('pessoa','Pessoa'),
        ('data_credito','Data do Crédito'),
        ('credito','Crédito')
    ]
    return render (request,"finance/credit_list.html",{
        'credits':credits,
        'colunas':colunas
    })

@login_required
@transaction.atomic 
def Accounts_list(request,id_accounts):
    venda = Venda.objects.filter(pessoa=id_accounts)
    conta = Accounts.objects.filter(pessoa_id=id_accounts)
    ordem_servico = Vendaservice.objects.filter(pessoa=id_accounts)
    
    accounts = PaymentMethod_Accounts.objects.filter(
        ( Q(venda__in = venda) | Q (conta__in = conta) | Q(ordem_servico__in = ordem_servico) ) 
        & Q(activeCredit = True) 
        )
    
    return render(request,'finance/ClientAccounts.html',{
        'accounts':accounts
    })
# CreditedClients.html

@login_required
@transaction.atomic
def deletePayment_Accounts(request,id):
    PaymentMethod_Accounts.objects.filter(id=id).delete()
    return JsonResponse({"message": "Pagamento deletado com sucesso!"}, status=200)

@login_required
def Cash_list(request):
    cash = CaixaDiario.objects.all().order_by('-id')

    paginator = Paginator(cash, 20)  
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'cash': page,
    }

    return render(request, 'finance/cash_list.html', context)

@login_required
def Cash_registry(request):
    if request.method == "POST":
        cash = CaixaDiarioForm(request.POST)
        user = CaixaDiario.objects.filter(
            Q(usuario_responsavel=request.user) & 
            Q(is_Active=1)
            )
        if user.exists():
            messages.error(request, f"Já Existe um Caixa aberto para {request.user.username}")
            return redirect('Cash_list')
        if cash.is_valid():
            caixa = cash.save(commit=False)
            caixa.usuario_responsavel = request.user
            caixa.is_Active = 1
            caixa.saldo_final = caixa.saldo_inicial
            cash.save()
            messages.success(request, 'Caixa Aberto Com Sucesso')
            return redirect('Cash_list')
    else:
        cash = CaixaDiarioForm()

    context = {
        'cash': cash,
    }
    return render(request, 'finance/cash_form.html', context)

@login_required
def Cash_Closeded(request, pk):
    if request.method == "POST":
        cash = CaixaDiarioForm(request.POST)
        user = FechamentoCaixaForm.objects.create()
        if user.exists():
            messages.error(request, f"Já Existe um Caixa aberto para {request.user.username}")
            return redirect('Cash_list')
        if cash.is_valid():
            caixa = cash.save(commit=False)
            caixa.usuario_responsavel = request.user
            caixa.is_Active = 1
            caixa.saldo_final = caixa.saldo_inicial
            cash.save()
            messages.success(request, 'Caixa Aberto Com Sucesso')
            return redirect('Cash_list')
    else:
        cash = CaixaDiarioForm()

    context = {
        'cash': cash,
    }
    return render(request, 'finance/cash_form.html', context)


@login_required
@transaction.atomic 
def cashFlow(request):
    cashMovement = CashMovement.objects.filter(
        Q(cash__usuario_responsavel=request.user)
    )
    
    context = {
        'CashMovement': cashMovement
    }
    return render(request, 'finance/cashFlow.html', context)


# @login_required
# @transaction.atomic 
# def Accounts_Create(request):
#     plannedAccount = request.GET.get("plannedAccount",'false')
#     print(plannedAccount)
#     verify = 0
#     installments = []
    

#     # PaymentMethodAccountsFormSet = inlineformset_factory(Accounts, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
#     PaymentMethodAccountsFormSet = inlineformset_factory(
#         Accounts,
#         PaymentMethod_Accounts,
#         form=PaymentMethodAccountsForm,
#         extra=1, 
#         can_delete=True,
#     )
#     if request.method == "POST":
        
#         post_data = request.POST.copy()
#         raw_data_planned_account = post_data.get('plannedAccount')
#         if raw_data_planned_account:
#             raw_date = post_data.get('date_init')
#             if raw_date:
#                 try:
#                     date_obj = datetime.strptime(raw_date,"%m/%Y")
#                     completed_date = date_obj.replace(day=1).date()
#                     post_data['date_init'] = completed_date.isoformat()
#                     form_Accounts = AccountsFormPlannedAccount(post_data)
#                 except ValueError as e:
#                     print("Erro ao tratar date_init",e)
#         else:
#             form_Accounts = AccountsForm(request.POST)
        
#         PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)
#         print(f"Total de formulários no formset: {len(PaymentMethod_Accounts_FormSet)}")
#         print(f"Formulários que foram alterados (has_changed): {[form.has_changed() for form in PaymentMethod_Accounts_FormSet]}")
#         # raw_date_init = post_data.get('date_init')
#         # if raw_date_init:
#         #     # Exemplo: garantir que está no formato YYYY-MM-DD
#         #     treated_date = raw_date_init.strip()  # aqui você pode usar um parser também
#         #     post_data['date_init'] = treated_date
        
#         if form_Accounts.is_valid():
#             print('oi')

#         if form_Accounts.is_valid() and PaymentMethod_Accounts_FormSet.is_valid():

#             # FIXME adicionar valor antigo e fazer comparação entre antigo, novo e gerar a parcela de desconto 

#             account = form_Accounts.save()
#             total_value = account.totalValue

#             print(f'\n\nQuantidade de formulários no FormSet: {len(PaymentMethod_Accounts_FormSet)}\n\n')

#             for form in PaymentMethod_Accounts_FormSet: 
#                 print('\npassou pelo if is_valid()\n')
#                 print(f'formulario unitario: {form}')
#                 if form.cleaned_data:
#                     print('\npassou pelo if cleaned_data()\n')

#                     parcela = form.cleaned_data['value']
#                     form.cleaned_data['value_old'] = parcela
#                     verify += parcela
#                     form_cleaned = form.save(commit=False)
#                     installments.append(form_cleaned)
#                 if float(verify) == float(total_value):
#                     for installment in installments:
#                         installment.conta = account
#                         installment.acc = True
#                         installment.save()
#                     messages.success(request,"Conta criada com sucesso.",extra_tags="successAccount")
#                     return redirect('AccountsPayable')
#                 else:
#                     print('\npassou pelo else verify()\n')

#                     form.add_error('value', f'O valor do somatorio das parcelas ({parcela}) é inferior ao Valor Total ({total_value}).')
#         else:
#             # print("Erros no form_Accounts:", form_Accounts.errors)
#             # print("Erros no PaymentMethod_Accounts_FormSet:", PaymentMethod_Accounts_FormSet.errors)
#             # Aqui, o formset não é válido, vamos imprimir os erros para diagnóstico
#             print(f"Erros no formulario de FormAccounts",form_Accounts.errors)
#             for form in PaymentMethod_Accounts_FormSet:
#                 print(f"Erros no formulário {form.instance}: {form.errors}")
#             print()
#             print("Erros do formset (non_field_errors):", PaymentMethod_Accounts_FormSet.non_form_errors())

#             # Opcional: Você pode exibir os erros de cada campo individualmente
#             for form in PaymentMethod_Accounts_FormSet:
#                 for field in form:
#                     if field.errors:
#                         print(f"Erro no campo {field.name}\t: {field.errors}")
            
#             # Retorna para o template com os erros
#             context = {
#                 'form_payment_account': PaymentMethod_Accounts_FormSet, 
#                 'tipo_conta': 'Receber'
#             }
#             return render(request, 'finance/AccountsPayform.html', context)
#     else: 
#         if plannedAccount =='false':
#             form_Accounts = AccountsForm()
#             # form_Accounts.fields['installment_Range'].choices = Accounts.INSTALLMENT_RANGE_CHOICES
#         else:
#             initial_data = {
#             'plannedAccount': plannedAccount,
#             }

#             form_Accounts = AccountsFormPlannedAccount(initial=initial_data)
       
#             # form_Accounts.fields['installment_Range'].choices = Accounts.INSTALLMENT_RANGE_CHOICES_PLANNED_ACCOUNT
#         PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())

#     context = {
#         'form_Accounts': form_Accounts,
#         'form_payment_account': PaymentMethod_Accounts_FormSet,
#         'Contas' : 'Contas a Pagar',
#         'tipo_conta': 'Pagar'
#     }
#     return render(request, 'finance/AccountsPayform.html', context)


def credit_total(request):
    query = request.GET.get('query')
    total = 0

    if query:
        credits = Credit.objects.filter(Q(person=query)).values_list('credit_value', flat=True)
        total = sum(credits)
    return JsonResponse({'credit_total': total})