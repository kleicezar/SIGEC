from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
import pdb

### CONTAS A PAGAR

# funcionando
@login_required
def Accounts_Create(request):
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

        print(request.POST) 

        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)

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
                    return redirect('AccountsPayable')
                else:
                    print('\npassou pelo else verify()\n')

                    form.add_error('value', f'O valor do somatorio das parcelas ({parcela}) é inferior ao Valor Total ({total_value}).')
        else:
            # print("Erros no form_Accounts:", form_Accounts.errors)
            # print("Erros no PaymentMethod_Accounts_FormSet:", PaymentMethod_Accounts_FormSet.errors)
            # Aqui, o formset não é válido, vamos imprimir os erros para diagnóstico
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
        form_Accounts = AccountsForm()
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
def Accounts_list(request):
    # Obtenha o termo de pesquisa da requisição
    search_query = request.GET.get('query', '') 

    # Filtrar os clientes com base no termo de pesquisa
    if search_query:
        account = PaymentMethod_Accounts.objects.filter(
        (   # campo pessoa
            Q(id__icontains=search_query) | 
            Q(conta__pessoa_id__id_FisicPerson_fk__name__icontains=search_query) | 
            Q(conta__pessoa_id__id_LegalPerson_fk__name_foreigner__icontains=search_query) | 
            Q(conta__pessoa_id__id_ForeignPerson_fk__fantasyName__icontains=search_query) | 
            Q(documentNumber__icontains=search_query)
        ),
        conta__acc = True 
    ).order_by('id')
    else:
        account = PaymentMethod_Accounts.objects.filter(acc = True).order_by('id') 

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
def update_Accounts(request, id_Accounts):
    payment_instance = get_object_or_404(PaymentMethod_Accounts, id=id_Accounts)
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

# funcionando
@login_required
def delete_Accounts(request, id_Accounts):
    # Recupera o accounte com o id fornecido
    account_deleta_pelo_amor_De_Deus = PaymentMethod_Accounts.objects.filter(id=id_Accounts,acc = True).delete() 
    return redirect('AccountsPayable')

### CONTAS A RECEBER

@login_required
def AccountsReceivable_Create(request):
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

        print(request.POST) 

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
                    return redirect('AccountsReceivable')
                else:
                    print('\npassou pelo else verify()\n')

                    form.add_error('value', f'O valor do somatorio das parcelas ({parcela}) é inferior ao Valor Total ({total_value}).')
        else:
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
        form_Accounts = AccountsForm()
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

    return render(request, 'finance/AccountsPay_list.html', {
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
def update_AccountsReceivable(request, id_Accounts):
    payment_instance = get_object_or_404(PaymentMethod_Accounts, id=id_Accounts)
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

# funcionando

@login_required
def delete_AccountsReceivable(request, id_Accounts):
    # Recupera o accounte com o id fornecido
    account_deleta_pelo_amor_De_Deus = PaymentMethod_Accounts.objects.filter(id=id_Accounts,acc = False).delete() #filter(acc = False)
    return redirect('AccountsReceivable')


def Credit_Update(request,id_client):
    person = Person.objects.get(id=id_client)
    if request.method == "POST":
        form_creditLimit = CreditForm(request.POST,instance=person)
        if form_creditLimit.is_valid():
            person.creditLimit = form_creditLimit.cleaned_data["creditLimit"]
            person.save()
            return redirect('CreditedClients')
        else:
            print("Erro no formulário de Limite de Crédito",form_creditLimit.errors)
    else:
        form_creditLimit = CreditForm(instance=person)

        context = {
            'form_creditLimit':form_creditLimit
        }
    return render(request,'finance/Creditform.html',context)


def CreditedClients_list(request):
    persons = Person.objects.all()
    return render(request,"finance/CreditedClients.html",{'persons':persons})


def Accounts_list(request,id_accounts):
    venda = Venda.objects.filter(pessoa=id_accounts)
    conta = Accounts.objects.filter(pessoa_id=id_accounts)
    ordem_servico = VendaService.objects.filter(pessoa=id_accounts)
    
    accounts = PaymentMethod_Accounts.objects.filter(
        ( Q(venda__in = venda) | Q (conta__in = conta) | Q(ordem_servico__in = ordem_servico) ) 
        & Q(activeCredit = True) 
        )
    
    return render(request,'finance/ClientAccounts.html',{
        'accounts':accounts
    })
# CreditedClients.html

def deletePayment_Accounts(request,id):
    PaymentMethod_Accounts.objects.filter(id=id).delete()
    return JsonResponse({"message": "Pagamento deletado com sucesso!"}, status=200)