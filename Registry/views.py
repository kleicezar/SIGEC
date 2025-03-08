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

### CLIENT

@login_required
def Client_Create(request):
    if request.method == "POST":
        form_address = AddressForm(request.POST)
        form_fisicPerson = FisicPersonForm(request.POST)
        form_legalPerson = LegalPersonModelForm(request.POST)
        form_foreigner = ForeignerModelForm(request.POST)
        form_Person = PersonForm(request.POST)

        # verificação e validação de endereço
        if form_address.is_valid():
            address = form_address.save()

        #verificação se o cadastro é valido 
        if form_Person.is_valid():

            # verificação em qual cadastro foi feito    
            if form_fisicPerson.is_valid():
                fisicPerson = form_fisicPerson.save(commit=False)
                fisicPerson.id_address_fk = address
                fisicPerson = form_fisicPerson.save()

                person = form_Person.save(commit=False)
                person.id_FisicPerson_fk = fisicPerson
                person.isActive = 1
                person.save()
                return redirect('Client')

            if form_legalPerson.is_valid():
                legalPerson = form_legalPerson.save(commit=False)
                legalPerson.id_address_fk = address
                legalPerson = form_legalPerson.save()

                person = form_Person.save(commit=False)
                person.id_LegalPerson_fk = legalPerson
                person.isActive = 1
                person.save()
                return redirect('Client')

            if form_foreigner.is_valid():
                foreigner = form_foreigner.save(commit=False)
                foreigner.id_address_fk = address
                foreigner = form_foreigner.save()

                person = form_Person.save(commit=False)
                person.id_ForeignPerson_fk = foreigner
                person.isActive = 1
                person.save()
                return redirect('Client')
            if not form_legalPerson.is_valid():
                print("Erros: ",form_legalPerson.errors)

    else: 
        form_address = AddressForm()
        form_fisicPerson = FisicPersonForm()
        form_legalPerson = LegalPersonModelForm()
        form_foreigner = ForeignerModelForm()
        form_Person = PersonForm()
        
    context = {
        'form_address': form_address,
        'form_fisicPerson': form_fisicPerson,
        'form_legalPerson': form_legalPerson,
        'form_foreigner': form_foreigner,
        'form_Person': form_Person
    }
    return render(request, 'registry/Clientform.html', context)

@login_required
def client_list(request):
    # Obtenha o termo de pesquisa da requisição
    print("Amigo estou aqui")
    search_query = request.GET.get('query', '')

    # Filtrar os clientes com base no termo de pesquisa
    if search_query:
        clients = Person.objects.filter(
        (
            Q(id__icontains=search_query) | 
            Q(id_FisicPerson_fk__name__icontains=search_query) | 
            Q(id_ForeignPerson_fk__name_foreigner__icontains=search_query) | 
            Q(id_LegalPerson_fk__fantasyName__icontains=search_query)
        ),
        isActive = True
    ).order_by('id')
    else:
        clients = Person.objects.all()

    # Configure o Paginator com o queryset filtrado
    paginator = Paginator(clients, 20)  # 5 itens por página
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'registry/client_list.html', {
        'clients': page,
        'query': search_query,  # Envie o termo de pesquisa para o template
    })


@login_required
def buscar_clientes(request):
    # """Busca clientes dinamicamente, retorna dados paginados em JSON."""
    query = request.GET.get('query', '').strip()  # Recebe a entrada do usuário
    page_num = request.GET.get('page', 1)  # Número da página atual

    # Realiza a busca com base no termo de pesquisa
    resultados = Person.objects.filter(
        Q(id__istartswith=query) | 
        Q(id_FisicPerson_fk__name__istartswith=query) | 
        Q(id_ForeignPerson_fk__name_foreigner__istartswith=query) | 
        Q(id_LegalPerson_fk__fantasyName__istartswith=query)
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