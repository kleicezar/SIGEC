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
from django.db import transaction
### CLIENT

@login_required
@transaction.atomic
def Client_Create(request):
    if request.method == "POST":
        # SALVA O LINK DA PAGINA ANTERIOR
        previous_url = request.session.get('previous_page', '/')

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
<<<<<<< Updated upstream
=======
            # log = log_db(request, action='c' ,type='01')

            person = form_Person.save(commit=False)
            person.id_address_fk = address
            person.isActive = 1
>>>>>>> Stashed changes

            # verificação em qual cadastro foi feito    
            if form_fisicPerson.is_valid():
                fisicPerson = form_fisicPerson.save(commit=False)
                fisicPerson.id_address_fk = address
                fisicPerson = form_fisicPerson.save()

<<<<<<< Updated upstream
                person = form_Person.save(commit=False)
                person.id_FisicPerson_fk = fisicPerson
                person.isActive = 1
=======
                # person = form_Person.save(commit=False)
                person.content_object = fisicPerson
                
                if person.email and person.password: 
                    person.id_user_fk = u
                    u = createUser(person.content_type.name, person.email, person.password)
                #     log_create_db(log, info_old=f'Cadastrou o Usuario {person.id_FisicPerson_fk.name}')
                # else:
                #     log_create_db(log, info_old=f'Cadastrou a Pessoa {person.id_FisicPerson_fk.name}')
                
>>>>>>> Stashed changes
                person.save()
                messages.success(request,"Cliente cadastrado com sucesso.",extra_tags="successClient")
                return redirect(previous_url)

            if form_legalPerson.is_valid():
                legalPerson = form_legalPerson.save(commit=False)
                legalPerson.id_address_fk = address
                legalPerson = form_legalPerson.save()

<<<<<<< Updated upstream
                person = form_Person.save(commit=False)
                person.id_LegalPerson_fk = legalPerson
                person.isActive = 1
=======
                # person = form_Person.save(commit=False)
                person.content_object = legalPerson
                if person.email and person.password: 
                    u = createUser(person.content_type.name, person.email, person.password)
                    person.id_user_fk = u
                #     log_create_db(log, info_old=f'Cadastrou o Usuario {person.id_LegalPerson_fk.fantasyName}')
                # else:
                #     log_create_db(log, info_old=f'Cadastrou a Pessoa {person.id_LegalPerson_fk.fantasyName}')
>>>>>>> Stashed changes
                person.save()
                messages.success(request,"Cliente cadastrado com sucesso.",extra_tags="successClient")
                return redirect(previous_url)

            if form_foreigner.is_valid():
                foreigner = form_foreigner.save(commit=False)
<<<<<<< Updated upstream
                foreigner.id_address_fk = address
                foreigner = form_foreigner.save()

                person = form_Person.save(commit=False)
                person.id_ForeignPerson_fk = foreigner
                person.isActive = 1
=======
                foreigner = form_foreigner.save()
                # person = form_Person.save(commit=False)
                person.content_object = foreigner
                if person.email and person.password: 
                    create = createUser(person.content_type.name, person.email, person.password,)
                    
                    person.id_user_fk = create
                    # log_create_db(log, info_old=f'Cadastrou o Usuario {person.id_ForeignPerson_fk.name_foreigner}')
                # else:
                    # log_create_db(log, info_old=f'Cadastrou a Pessoa {person.id_ForeignPerson_fk.name_foreigner}')
                    
>>>>>>> Stashed changes
                person.save()
                messages.success(request,"Cliente cadastrado com sucesso.",extra_tags="successClient")
                return redirect(previous_url)
            if not form_legalPerson.is_valid():
                print("Erros: ",form_legalPerson.errors)

    else: 
        if 'HTTP_REFERER' in request.META:
            # SALVA A PAGINA ANTERIOR
            request.session['previous_page'] = request.META['HTTP_REFERER']
            print(request.session['previous_page'])
        

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
    search_query = request.GET.get('query', '')

    # Filtrar os clientes com base no termo de pesquisa
    if search_query:
        clients = Person.objects.filter(
<<<<<<< Updated upstream

        (
            Q(id__icontains=search_query) | 
            Q(id_FisicPerson_fk__name__icontains=search_query) | 
            Q(id_ForeignPerson_fk__name_foreigner__icontains=search_query) | 
            Q(id_LegalPerson_fk__fantasyName__icontains=search_query) 
            
        ) 
        & Q(isActive = False)
=======
            (
                Q(id__startswith=search_query) |
                Q(nome_cliente__istartswith=search_query)
            ) &
            Q(isActive = True),
        )
    else:
        clients = Person.objects.filter(
                Q(isActive = True),
            ).select_related('content_type')
>>>>>>> Stashed changes
        
        ).order_by('id')
    
    else:
        clients = Person.objects.filter(
            isActive = True
        )

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
        (
            Q(id__istartswith=query) | 
            Q(content_object__name__istartswith=query)
        )
        & Q(isActive = True)
    ).order_by('id')

    # Serializa os resultados em uma lista de dicionários
    clients = [
        {
            'id': cliente.id,
            'name': cliente.content_object.name,
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
@transaction.atomic
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
            messages.success(request,"Cliente atualizado com sucesso.",extra_tags="successClient")
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
@transaction.atomic
def delete_client(request, id_client):
    # Recupera o cliente com o id fornecido
    client = get_object_or_404(Person, id=id_client)
    client.isActive = False
    client.save()
<<<<<<< Updated upstream
=======
    # log = Log.objects.create(
    #             user=request.user,
    #             date=datetime.now(),
    #             action='d',
    #             type='01'
    #         )
    # if client.id_FisicPerson_fk:
    #     Info_logs.objects.create(log_principal=log, info_old=f'Inativou a Pessoa {client.id_FisicPerson_fk.name}')
    # if client.id_ForeignPerson_fk:
    #     Info_logs.objects.create(log_principal=log, info_old=f'Inativou a Pessoa {client.id_ForeignPerson_fk.name_foreigner}')
    # if client.id_LegalPerson_fk:
    #     Info_logs.objects.create(log_principal=log, info_old=f'Inativou a Pessoa {client.id_LegalPerson_fk.fantasyName}')
>>>>>>> Stashed changes
    messages.success(request,"Cliente deletado com sucesso.",extra_tags="successClient")
    return redirect('Client')

@login_required
def get_client(request, id_client):
<<<<<<< Updated upstream
    person = Person.objects.get(id=id_client)
    if person.id_FisicPerson_fk:
=======
    log = Log.objects.create(
            user=request.user,
            date=datetime.now(),
            action='r',
            type='01'
        )
    person = Person.objects.get(id=id_client)
    if person.content_object == 'fisicperson':
>>>>>>> Stashed changes
        client = {
                'id': person.id,
                'name': ( person.content_object.name if person.content_object else 'Nome não disponível' ),
                'cpf': ( person.content_object.cpf if person.content_object else 'Cadastro de Pessoa Fisica - CPF indisponível'),
                'rg': ( person.content_object.rg if person.content_object else 'Registro Geral - RG indisponível'),
                'dateOfBirth': ( person.content_object.dateOfBirth if person.content_object else 'Data de Aniversario indisponível'),
                'WorkPhone': person.WorkPhone,
                'PersonalPhone': person.PersonalPhone,
                'Site': person.site if person.site else 'Não Informado',
                'Salesman': person.salesman if person.salesman else 'Não Informado',
                'CreditLimit': person.creditLimit if person.creditLimit else 'Não Informado',
                }
<<<<<<< Updated upstream
    if person.id_LegalPerson_fk:
=======
        # log_info = Info_logs.objects.create(log_principal=log, info_old=f'Visualizou a Pessoa {person.id_FisicPerson_fk.name}')
        
    if person.content_object == 'legalperson':
>>>>>>> Stashed changes
        client = {
                'id': person.id,
                'name': ( person.content_object.name if person.content_object else 'Nome indisponível'),
                'cnpj':( person.content_object.cnpj if person.content_object else 'CNPJ indisponível'),
                'socialReason':( person.content_object.socialReason if person.content_object else 'Razão Social indisponível'),
                'StateRegistration':( person.content_object.StateRegistration if person.content_object else 'Inscrição Estadual indisponível'),
                'typeOfTaxpayer':( person.content_object.typeOfTaxpayer if person.content_object else 'Tipo de Contribuinte indisponível'),
                'MunicipalRegistration':( person.content_object.MunicipalRegistration if person.content_object else 'Inscrição Municipal indisponível'),
                'suframa':( person.content_object.suframa if person.content_object else 'Numero da Suframa indisponível'),
                'Responsible':( person.content_object.Responsible if person.content_object else 'Nome do Responsavel indisponível'),
                'WorkPhone': person.WorkPhone,
                'PersonalPhone': person.PersonalPhone,
                'Site': person.site if person.site else 'Não Informado',
                'Salesman': person.salesman if person.salesman else 'Não Informado',
                'CreditLimit': person.creditLimit if person.creditLimit else 'Não Informado',
            }
<<<<<<< Updated upstream
        
    if person.id_ForeignPerson_fk:
=======
        log_info = Info_logs.objects.create(log_principal=log, info_old=f'Visualizou a Pessoa {person.content_object.fantasyName}')
               

    if isinstance(person.content_object, ForeignPerson):
>>>>>>> Stashed changes
        client = {
                'id': person.id,
                'name': getattr(person.content_object, 'name', 'Nome não disponível'),
                'num_foreigner': getattr(person.content_object, 'num_foreigner', 'Documento estrangeiro não disponível'),
                'WorkPhone': person.WorkPhone,
                'PersonalPhone': person.PersonalPhone,
                'Site': person.site if person.site else 'Não Informado',
                'Salesman': person.salesman if person.salesman else 'Não Informado',
                'CreditLimit': person.creditLimit if person.creditLimit else 'Não Informado',
                'client': 'foreignperson'
            }
<<<<<<< Updated upstream
=======
    #     log_info = Info_logs.objects.create(log_principal=log, info_old=f'Visualizou a Pessoa {person.id_ForeignPerson_fk.name_foreigner}')
    # for chave, valor in client.items():
    #     print(f'chave:{chave} valor:{valor}')
    # print(f'valor id :{client[id]}') 
    print(f"Tipo do objeto relacionado: {(client['name'])}")
    print(f"Valor: {client['num_foreigner']}")
    # log.save() ,log_info.save()
>>>>>>> Stashed changes
        
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