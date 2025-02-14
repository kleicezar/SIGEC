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

### CONTAS A PAGAR

# funcionando
@login_required
def Accounts_Create(request):
    verify = 0
    installments = []
    PaymentMethodAccountsFormSet = inlineformset_factory(Accounts, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    if request.method == "POST":
        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)
        print(f'deu certo ate aqui "primeiro IF"')

        if form_Accounts.is_valid() and PaymentMethod_Accounts_FormSet.is_valid():
            account = form_Accounts.save()
            print(f'deu certo ate aqui "segundo IF"')

            total_value = account.totalValue
            for form in PaymentMethod_Accounts_FormSet:
                if form.cleaned_data:
                    print(f'deu certo ate aqui "terceiro IF"')
                    parcela = form.cleaned_data['value']
                    verify += parcela
                    form_cleaned = form.save(commit=False)
                    installments.append(form_cleaned)
           
            if float(verify) == float(total_value):
                for installment in installments:
                    print(f'deu certo ate aqui "vai salvar"')
                    installment.conta = account
                    installment.acc = True
                    installment.save()
                return redirect('AccountsPayable')
            else:
                form.add_error('value', f'O valor do somatorio das parcelas ({parcela}) é inferior ao Valor Total ({total_value}).')
    else: 
        form_Accounts = AccountsForm()
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        
    context = {
        'form_Accounts': form_Accounts,
        'form_payment_account': PaymentMethod_Accounts_FormSet,
        'Contas' : 'Contas a Pagar'

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
        'form_accounts': page,
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
    'interestPercent':paymentMethod_Accounts.interestPercent,
    'interestValue':paymentMethod_Accounts.interestValue,
    'finePercent':paymentMethod_Accounts.finePercent,
    'fineValue':paymentMethod_Accounts.fineValue,
    }
    
        
    return render(request, 'finance/AccountsPay_GET.html', {'client': client})

@login_required
def update_Accounts(request, id_client):
    # Buscar o cliente e os dados relacionados
    selected_form = 'a'
    try:
        person = Person.objects.get(id=id_client)
        # print(person)
        if person.id_FisicPerson_fk:
            fisicPerson = person.id_FisicPerson_fk
            address = person.id_FisicPerson_fk.id_address_fk
            selected_form = "Pessoa Fisica"
            legalPerson = None
            foreigner = None
        else:
            fisicPerson = None
            if person.id_LegalPerson_fk:
                legalPerson = person.id_LegalPerson_fk
                address = person.id_LegalPerson_fk.id_address_fk
                selected_form = "Pessoa Juridica"
                foreigner = None
            else:
                legalPerson = None
                if person.id_ForeignPerson_fk:
                    foreigner = person.id_ForeignPerson_fk
                    address = person.id_ForeignPerson_fk.id_address_fk
                    selected_form = "Estrangeiro"
                else:
                    foreigner = None
                    selected_form = ""

    except Person.DoesNotExist:
        return redirect('Client')  # Redirecionar para pagina inicial de clientes

    if request.method == "POST":
        form_address = AddressForm(request.POST, instance=address)
        form_fisicPerson = FisicPersonForm(request.POST, instance=fisicPerson)
        form_legalPerson = LegalPersonModelForm(request.POST, instance=legalPerson)
        form_foreigner = ForeignerModelForm(request.POST, instance=foreigner)
        form_Person = PersonForm(request.POST, instance=person)

        # Atualização do endereço
        if form_address.is_valid():
            address = form_address.save()

        # Atualização dos dados principais
        if form_Person.is_valid():
            if fisicPerson and form_fisicPerson.is_valid():
                fisicPerson = form_fisicPerson.save(commit=False)
                fisicPerson.id_address_fk = address
                fisicPerson.save()

                person = form_Person.save(commit=False)
                person.id_FisicPerson_fk = fisicPerson
                person.save()

            elif legalPerson and form_legalPerson.is_valid():
                legalPerson = form_legalPerson.save(commit=False)
                legalPerson.id_address_fk = address
                legalPerson.save()

                person = form_Person.save(commit=False)
                person.id_LegalPerson_fk = legalPerson
                person.save()

            elif foreigner and form_foreigner.is_valid():
                foreigner = form_foreigner.save(commit=False)
                foreigner.id_address_fk = address
                foreigner.save()

                person = form_Person.save(commit=False)
                person.id_ForeignPerson_fk = foreigner
                person.save()

            return redirect('Client')  # Redirecionar após salvar as alterações
    else:
        # Preencher os formulários com os dados existentes
        form_address = AddressForm(instance=address)
        form_fisicPerson = FisicPersonForm(instance=fisicPerson)
        form_legalPerson = LegalPersonModelForm(instance=legalPerson)
        form_foreigner = ForeignerModelForm(instance=foreigner)
        form_Person = PersonForm(instance=person)

    context = {
        'form_address': form_address,
        'form_fisicPerson': form_fisicPerson,
        'form_legalPerson': form_legalPerson,
        'form_foreigner': form_foreigner,
        'form_Person': form_Person,
        'selected_form': selected_form,
    }
    return render(request, 'registry/ClientformUpdate.html', context)

# funcionando
@login_required
def delete_Accounts(request, id_Accounts):
    # Recupera o accounte com o id fornecido
    account_deleta_pelo_amor_De_Deus = PaymentMethod_Accounts.objects.filter(id=id_Accounts,acc = True).delete() 
    return redirect('AccountsPayable')

### CONTAS A RECEBER

# funcionando
@login_required
def AccountsReceivable_Create(request):
    verify = 0
    installments = []
    PaymentMethodAccountsFormSet = inlineformset_factory(Accounts, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    if request.method == "POST":
        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)

        if form_Accounts.is_valid() and PaymentMethod_Accounts_FormSet.is_valid():
            account = form_Accounts.save()
            total_value = account.totalValue
            for form in PaymentMethod_Accounts_FormSet:
                if form.cleaned_data:
                    parcela = form.cleaned_data['value']
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
                form.add_error('value', f'O valor do somatorio das parcelas ({parcela}) é inferior ao Valor Total ({total_value}).')
    else: 
        form_Accounts = AccountsForm()
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        
    context = {
        'form_Accounts': form_Accounts,
        'form_payment_account': PaymentMethod_Accounts_FormSet,
        'Contas' : 'Contas a Receber'
    }
    return render(request, 'finance/AccountsPayform.html', context)

# funcionando
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
    'interestPercent':paymentMethod_Accounts.interestPercent,
    'interestValue':paymentMethod_Accounts.interestValue,
    'finePercent':paymentMethod_Accounts.finePercent,
    'fineValue':paymentMethod_Accounts.fineValue,
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
            if not payment_instance.interestPercent:
                payment_instance.interestPercent = None
            if not payment_instance.interestValue:
                payment_instance.interestValue = None
            if not payment_instance.finePercent:
                payment_instance.finePercent = None
            if not payment_instance.fineValue:
                payment_instance.fineValue = None

            payment_instance.save()

            return redirect('AccountsReceivable')  # Redirecionar após salvar
        else:
            print("Erros no payment_form_instance:", payment_form_instance.errors)
            print()
            print("Erros no accounts_form_instance:", accounts_form_instance.errors)
            print()


    else:
        accounts_form_instance = AccountsFormUpdate(instance=accounts_instance)
        payment_form_instance = PaymentMethodAccountsForm(instance=payment_instance)

    context = {
        'form_Accounts': accounts_form_instance,
        'form_paymentMethodAccounts': payment_form_instance,
    }

    return render(request, 'finance/AccountsPayformUpdate.html', context)
    # payment_instance = get_object_or_404(PaymentMethod_Accounts, id=id_Accounts)
    # accounts_instance = get_object_or_404(Accounts, id=payment_instance.conta_id)
    # if request.method == "POST":  
    #     payment_form_instance = PaymentMethodAccountsForm(request.POST, instance=payment_instance)

        # accounts_form_instance = AccountsForm(
        #     request.POST, 
        #     instance=accounts_instance,
        #     initial={
        #         'numberOfInstallments': accounts_instance.numberOfInstallments,
        #         'installment_Range': accounts_instance.installment_Range,
        #         'totalValue': accounts_instance.totalValue,
        #         'date_init': accounts_instance.date_init
        #     }
        # )

    #     # accounts_form_instance.numberOfInstallments = accounts_instance.numberOfInstallments
    #     # accounts_form_instance.installment_Range = accounts_instance.installment_Range
    #     # accounts_form_instance.totalValue = accounts_instance.totalValue
    #     # accounts_form_instance.date_init = accounts_instance.date_init

    #     print(accounts_instance.date_init)
    #     print('funciona pelo amor de Deus')
    #     # print(payment_form_instance.errors)
    #     print(accounts_form_instance.errors)

    #     if payment_form_instance.is_valid() and accounts_form_instance.is_valid():
    #         print('funciona pelo amor de Deus')
    #         accounts_form_instance.save()
    #         payment_form_instance.save(commit=False)
    #         if payment_form_instance.interestPercent == '':
    #             print(payment_form_instance.interestPercent)
    #             payment_form_instance.interestPercent = None
    #         if payment_form_instance.interestValue == 0: 
    #             print(payment_form_instance.interestValue)
    #             payment_form_instance.interestValue = None
    #         if payment_form_instance.finePercent == '':
    #             print(payment_form_instance.finePercent)
    #             payment_form_instance.finePercent = None
    #         if payment_form_instance.fineValue == 0:
    #             print(payment_form_instance.fineValue)
    #             payment_form_instance.fineValue = None
    #         payment_form_instance.save()

    #         return redirect('AccountsReceivable')  # Redirecionar após salvar as alterações
    # else:
    #     # Preencher os formulários com os dados existentes
    #     accounts_form_instance = AccountsForm(instance=accounts_instance)
    #     payment_form_instance = PaymentMethodAccountsForm(instance=payment_instance)

    # context = {
    #     'form_Accounts': accounts_form_instance,
    #     'form_paymentMethodAccounts': payment_form_instance,
    # }
 
    # return render(request, 'finance/AccountsPayformUpdate.html', context)

# funcionando
@login_required
def delete_AccountsReceivable(request, id_Accounts):
    # Recupera o accounte com o id fornecido
    account_deleta_pelo_amor_De_Deus = PaymentMethod_Accounts.objects.filter(id=id_Accounts,acc = False).delete() #filter(acc = False)
    return redirect('AccountsReceivable')
