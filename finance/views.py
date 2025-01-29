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

@login_required
def AccountsPayable_Create(request):
    PaymentMethodAccountsPayableFormSet = inlineformset_factory(AccountsPayable, PaymentMethod_AccountsPayable, form=PaymentMethodAccountsPayableForm, extra=1, can_delete=True)
    if request.method == "POST":
        form_AccountsPayable = AccountsPayableForm(request.POST)
        PaymentMethod_AccountsPayable_FormSet = PaymentMethodAccountsPayableFormSet(request.POST)
        if form_AccountsPayable.is_valid() and PaymentMethod_AccountsPayable_FormSet.is_valid():
          for form in PaymentMethod_AccountsPayable_FormSet:
                if form.cleaned_data:
                    produto = form.cleaned_data['product']
                    quantidade = form.cleaned_data['quantidade']
                    if produto.current_quantity < quantidade:
                        estoque_suficiente = False
                        form.add_error('quantidade', f'Não há estoque suficiente para o produto {produto.description}. Estoque disponível: {produto.current_quantity}.')
        elif not form_AccountsPayable.is_valid():
            print("Erros",form_AccountsPayable.errors)
        elif not PaymentMethod_AccountsPayable_FormSet.is_valid():
            print("Erros",PaymentMethod_AccountsPayable_FormSet.errors)
    else: 
        form_AccountsPayable = AccountsPayableForm()
        PaymentMethod_AccountsPayable_FormSet = PaymentMethodAccountsPayableFormSet(queryset=PaymentMethod_AccountsPayable.objects.none())
        
    context = {
        'form_AccountsPayable': form_AccountsPayable,
        'form_payment_account': PaymentMethod_AccountsPayable_FormSet
    }
    return render(request, 'finance/AccountsPayform.html', context)

@login_required
def AccountsPayable_list(request):
    # Obtenha o termo de pesquisa da requisição
    search_query = request.GET.get('query', '')

    # Filtrar os clientes com base no termo de pesquisa
    if search_query:
        accountPayable = AccountsPayable.objects.filter(
        (   # campo pessoa
            Q(id__icontains=search_query) | 
            Q(pessoa_id__id_FisicPerson_fk__name__icontains=search_query) | 
            Q(pessoa_id__id_LegalPerson_fk__name_foreigner__icontains=search_query) | 
            Q(pessoa_id__id_ForeignPerson_fk__fantasyName__icontains=search_query) | 
            Q(documentNumber__icontains=search_query)
        ),
        isActive = True 
    ).order_by('id')
    else:
        accountPayable = AccountsPayable.objects.all()

    for i in accountPayable:
        print(accountPayable) 
    # Configure o Paginator com o queryset filtrado
    paginator = Paginator(accountPayable, 20)  # 5 itens por página
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'finance/AccountsPay_list.html', {
        'accountsPayable': page,
        'query': search_query,  # Envie o termo de pesquisa para o template
    })

# para futuros testes
# INSERT INTO finance_accountspayable(
#     pessoa_id, 
#     chartofaccounts_id, 
#     documentnumber, 
#     date_account, 
#     numberofinstallments, 
#     valueofinstallments, 
#     totalvalue, 
#     peoplewatching, 
#     systemwatching
# )
# VALUES (
#     1, -- ID de uma pessoa existente na tabela `Person`
#     NULL, -- `chartOfAccounts` será NULL
#     12345, -- Número do documento
#     '2025-01-23 15:30:00', -- Data da conta a pagar
#     12, -- Número de parcelas
#     500.00, -- Valor de cada parcela
#     6000.00, -- Valor total
#     'Cliente pediu para ajustar o prazo.', -- Observação para a pessoa
#     'Sistema gerou conta automaticamente.' -- Observação para o sistema
# );

### CONTAS A RECEBER

@login_required
def AccountsReceivable_Create(request):
    PaymentMethodAccountsReceivableFormSet = inlineformset_factory(AccountsReceivable, PaymentMethod_AccountsReceivable, form=PaymentMethodAccountsReceivableForm, extra=1, can_delete=True)
    if request.method == "POST":
        form_AccountsReceivable = AccountsReceivableForm(request.POST)
        PaymentMethod_AccountsReceivable_FormSet = PaymentMethodAccountsReceivableFormSet(request.POST)
        if form_AccountsReceivable.is_valid() and PaymentMethod_AccountsReceivable_FormSet.is_valid():
          for form in PaymentMethod_AccountsReceivable_FormSet:
                if form.cleaned_data:
                    produto = form.cleaned_data['product']
                    quantidade = form.cleaned_data['quantidade']
                    if produto.current_quantity < quantidade:
                        estoque_suficiente = False
                        form.add_error('quantidade', f'Não há estoque suficiente para o produto {produto.description}. Estoque disponível: {produto.current_quantity}.')
    else: 
        form_AccountsReceivable = AccountsReceivableForm()
        PaymentMethod_AccountsReceivable_FormSet = PaymentMethodAccountsReceivableFormSet(queryset=PaymentMethod_AccountsReceivable.objects.none())
        
    context = {
        'form_AccountsReceivable': form_AccountsReceivable,
        'form_payment_account': PaymentMethod_AccountsReceivable_FormSet
    }
    return render(request, 'finance/AccountsReceivableform.html', context)

@login_required
def AccountsReceivable_list(request):
    # Obtenha o termo de pesquisa da requisição
    search_query = request.GET.get('query', '')

    # Filtrar os clientes com base no termo de pesquisa
    if search_query:
        accountReceivable = AccountsReceivable.objects.filter(
        (   # campo pessoa
            Q(id__icontains=search_query) | 
            Q(pessoa_id__id_FisicPerson_fk__name__icontains=search_query) | 
            Q(pessoa_id__id_LegalPerson_fk__name_foreigner__icontains=search_query) | 
            Q(pessoa_id__id_ForeignPerson_fk__fantasyName__icontains=search_query) | 
            Q(documentNumber__icontains=search_query)
        ),
        isActive = True 
    ).order_by('id')
    else:
        accountReceivable = AccountsReceivable.objects.all()

    for i in accountReceivable:
        print(accountReceivable) 
    # Configure o Paginator com o queryset filtrado
    paginator = Paginator(accountReceivable, 20)  # 5 itens por página
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'finance/AccountsReceivable_list.html', {
        'accountsReceivable': page,
        'query': search_query,  # Envie o termo de pesquisa para o template
    })


#+------------------------------------------+
#
#+------------------------------------------+

@login_required
def buscar_clientes(request):
    # """Busca clientes dinamicamente, retorna dados paginados em JSON."""
    query = request.GET.get('query', '').strip()  # Recebe a entrada do usuário
    page_num = request.GET.get('page', 1)  # Número da página atual

    # Realiza a busca com base no termo de pesquisa
    resultados = Person.objects.filter(
        Q(id__icontains=query) | 
        Q(id_FisicPerson_fk__name__icontains=query) | 
        Q(id_ForeignPerson_fk__name_foreigner__icontains=query) | 
        Q(id_LegalPerson_fk__fantasyName__icontains=query)
    ).order_by('id')

    # Serializa os resultados em uma lista de dicionários
    clients = [
        {
            'id': cliente.id,
            'name': (
                cliente.id_FisicPerson_fk.name if cliente.id_FisicPerson_fk else 
                (cliente.id_ForeignPerson_fk.name_foreigner if cliente.id_ForeignPerson_fk else 
                (cliente.id_LegalPerson_fk.fantasyName if cliente.id_LegalPerson_fk else 'Nome não disponível'))),
            'WorkPhone': cliente.WorkPhone,
            'PersonalPhone': cliente.PersonalPhone,
        }
        for cliente in resultados
    ]

    # Paginação
    usuario_paginator = Paginator(clients, 20)  # 20 resultados por página
    page = usuario_paginator.get_page(page_num)

    # Constrói a resposta JSON
    response_data = {
        'clientes': list(page.object_list),
        'pagination': {
            'has_previous': page.has_previous(),
            'previous_page': page.previous_page_number() if page.has_previous() else None,
            'has_next': page.has_next(),
            'next_page': page.next_page_number() if page.has_next() else None,
            'current_page': page.number,
            'total_pages': usuario_paginator.num_pages,
        },
        'message': f"{len(clients)} Clientes encontrados." if page.object_list else "Nenhum cliente encontrado."
    }
    return JsonResponse(response_data)

@login_required
def update_client(request, id_client):
    # Buscar o cliente e os dados relacionados
    selected_form = 'a'
    try:
        person = Person.objects.get(id=id_client)
        print(person)
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
    print(selected_form)
    print(type(selected_form))

    return render(request, 'registry/ClientformUpdate.html', context)

@login_required
def delete_client(request, id_client):
    # Recupera o cliente com o id fornecido
    client = get_object_or_404(Person, id=id_client)
    client.delete()
    return redirect('Client')

@login_required
def get_client(request, id_client):
    person = Person.objects.get(id=id_client)
    if person.id_FisicPerson_fk:
        client = {
                'id': person.id,
                'name': ( person.id_FisicPerson_fk.name if person.id_FisicPerson_fk else 'Nome não disponível' ),
                'cpf': ( person.id_FisicPerson_fk.cpf if person.id_FisicPerson_fk else 'Cadastro de Pessoa Fisica - CPF indisponível'),
                'rg': ( person.id_FisicPerson_fk.rg if person.id_FisicPerson_fk else 'Registro Geral - RG indisponível'),
                'dateOfBirth': ( person.id_FisicPerson_fk.dateOfBirth if person.id_FisicPerson_fk else 'Data de Aniversario indisponível'),
                'WorkPhone': person.WorkPhone,
                'PersonalPhone': person.PersonalPhone,
                'Site': person.site if person.site else 'Não Informado',
                'Salesman': person.salesman if person.salesman else 'Não Informado',
                'CreditLimit': person.creditLimit if person.creditLimit else 'Não Informado',
                'id_FisicPerson_fk': 1,
                }
    if person.id_LegalPerson_fk:
        client = {
                'id': person.id,
                'name': ( person.id_LegalPerson_fk.fantasyName if person.id_LegalPerson_fk else 'Nome indisponível'),
                'cnpj':( person.id_LegalPerson_fk.cnpj if person.id_LegalPerson_fk else 'CNPJ indisponível'),
                'socialReason':( person.id_LegalPerson_fk.socialReason if person.id_LegalPerson_fk else 'Razão Social indisponível'),
                'StateRegistration':( person.id_LegalPerson_fk.StateRegistration if person.id_LegalPerson_fk else 'Inscrição Estadual indisponível'),
                'typeOfTaxpayer':( person.id_LegalPerson_fk.typeOfTaxpayer if person.id_LegalPerson_fk else 'Tipo de Contribuinte indisponível'),
                'MunicipalRegistration':( person.id_LegalPerson_fk.MunicipalRegistration if person.id_LegalPerson_fk else 'Inscrição Municipal indisponível'),
                'suframa':( person.id_LegalPerson_fk.suframa if person.id_LegalPerson_fk else 'Numero da Suframa indisponível'),
                'Responsible':( person.id_LegalPerson_fk.Responsible if person.id_LegalPerson_fk else 'Nome do Responsavel indisponível'),
                'WorkPhone': person.WorkPhone,
                'PersonalPhone': person.PersonalPhone,
                'Site': person.site if person.site else 'Não Informado',
                'Salesman': person.salesman if person.salesman else 'Não Informado',
                'CreditLimit': person.creditLimit if person.creditLimit else 'Não Informado',
                'id_LegalPerson_fk': 1,
            }
        
    if person.id_ForeignPerson_fk:
        client = {
                'id': person.id,
                'name_foreigner': ( person.id_ForeignPerson_fk.name_foreigner if person.id_ForeignPerson_fk else 'Nome não disponível'),
                'num_foreigner': ( person.id_ForeignPerson_fk.num_foreigner if person.id_ForeignPerson_fk else 'Numero do Documento Estrangeiro não disponível'),
                'WorkPhone': person.WorkPhone,
                'PersonalPhone': person.PersonalPhone,
                'Site': person.site if person.site else 'Não Informado',
                'Salesman': person.salesman if person.salesman else 'Não Informado',
                'CreditLimit': person.creditLimit if person.creditLimit else 'Não Informado',
                'id_ForeignPerson_fk': 1,
            }
        
    return render(request, 'registry/Client_Get.html', {'client': client})

    print('-------------------')
    # print(client.id_FisicPerson_fk | None)
    # print(client.id_LegalPerson_fk | None)
    # print(client.id_ForeignPerson_fk | None)
    print(client)
    print('-------------------')

        # clients = Person.objects.filter( Q(id__icontains=query) | 
        # Q(id_FisicPerson_fk__name__icontains=query) | 
        # Q(id_ForeignPerson_fk__name_foreigner__icontains=query) | 
        # Q(id_LegalPerson_fk__fantasyName__icontains=query))
        

    #     form_address = AddressForm(request.POST, instance=address)
    #     form_fisicPerson = FisicPersonForm(request.POST, instance=fisicPerson)
    #     form_legalPerson = LegalPersonModelForm(request.POST, instance=legalPerson)
    #     form_foreigner = ForeignerModelForm(request.POST, instance=foreigner)
    #     form_Person = PersonForm(request.POST, instance=person)
    # else:
    #     form = CombinedForm()

    # client = [
    #     {
    #         'id': person.id,
    #         'name': (    person.id_FisicPerson_fk.name if person.id_FisicPerson_fk else 
    #                     (person.id_ForeignPerson_fk.name_foreigner if person.id_ForeignPerson_fk else 
    #                     (person.id_LegalPerson_fk.fantasyName if person.id_LegalPerson_fk else 'Nome não disponível'))),
    #         'WorkPhone': person.WorkPhone,
    #         'PersonalPhone': person.PersonalPhone,
    #         'Site': person.site if person.site else 'Não Informado',
    #         'Salesman': person.salesman if person.salesman else 'Não Informado',
    #         'CreditLimit': person.salesman if person.salesman else 'Não Informado',
    #         }
    #     ]

    return HttpResponse(client)

### TECNICOS

@login_required
def search_tech(request):
    # """Busca clientes dinamicamente, retorna dados paginados em JSON."""
    query = request.GET.get('query', '').strip()  # Recebe a entrada do usuário
    page_num = request.GET.get('page', 1)  # Número da página atual

    # Realiza a busca com base no termo de pesquisa
    if query:
        resultados = Person.objects.filter(
            (
                Q(id__icontains=query) | 
                Q(id_FisicPerson_fk__name__icontains=query) | 
                Q(id_ForeignPerson_fk__name_foreigner__icontains=query) | 
                Q(id_LegalPerson_fk__fantasyName__icontains=query),
            ),
            isTechnician=True, 
            isActive=True
        ).order_by('id')
    else:  # Retorna um queryset vazio caso não haja busca
        resultados = Person.objects.filter(
            (
                Q(id__icontains=query) | 
                Q(id_FisicPerson_fk__name__icontains=query) | 
                Q(id_ForeignPerson_fk__name_foreigner__icontains=query) | 
                Q(id_LegalPerson_fk__fantasyName__icontains=query),
            ),
            isTechnician=True, 
            isActive=True
        ).order_by('id')

    # Serializa os resultados em uma lista de dicionários
    clients = [
        { 
            'id': cliente.id,
            'name': (
                cliente.id_FisicPerson_fk.name if cliente.id_FisicPerson_fk else 
                (cliente.id_ForeignPerson_fk.name_foreigner if cliente.id_ForeignPerson_fk else 
                (cliente.id_LegalPerson_fk.fantasyName if cliente.id_LegalPerson_fk else 'Nome não disponível'))),
            'WorkPhone': cliente.WorkPhone,
            'PersonalPhone': cliente.PersonalPhone,
        }
        for cliente in resultados
    ]

    # Paginação
    usuario_paginator = Paginator(clients, 20)  # 20 resultados por página
    page = usuario_paginator.get_page(page_num)

    # Constrói a resposta JSON
    response_data = { 
        'clientes': list(page.object_list),
        'pagination': {
            'has_previous': page.has_previous(),
            'previous_page': page.previous_page_number() if page.has_previous() else None,
            'has_next': page.has_next(),
            'next_page': page.next_page_number() if page.has_next() else None,
            'current_page': page.number,
            'total_pages': usuario_paginator.num_pages,
        },
        'message': f"{len(clients)} Clientes encontrados." if page.object_list else "Nenhum cliente encontrado."
    }
    return JsonResponse(response_data)