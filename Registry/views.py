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


# ### CLIENT

# instagram 
# SBA
# Acre tratores


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
                person.isActive = person.isClient = person.isSupllier = 1
                person.isUser = person.isEmployee = person.isFormer_employee = person.isCarrier = person.isDelivery_man = person.isTechnician = 0
                person.save()

            if form_legalPerson.is_valid():
                legalPerson = form_legalPerson.save(commit=False)
                legalPerson.id_address_fk = address
                legalPerson = form_legalPerson.save()

                person = form_Person.save(commit=False)
                person.id_LegalPerson_fk = legalPerson
                person.isActive = person.isClient = person.isSupllier = 1
                person.isUser = person.isEmployee = person.isFormer_employee = person.isCarrier = person.isDelivery_man = person.isTechnician = 0
                person.save()

            if form_foreigner.is_valid():
                foreigner = form_foreigner.save(commit=False)
                foreigner.id_address_fk = address
                foreigner = form_foreigner.save()

                person = form_Person.save(commit=False)
                person.id_ForeignPerson_fk = foreigner
                person.isActive = person.isClient = person.isSupllier = 1
                person.isUser = person.isEmployee = person.isFormer_employee = person.isCarrier = person.isDelivery_man = person.isTechnician = 0
                person.save()
                return redirect('Client')

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
    # Cria o formulário de pesquisa
    form = ClientSearchForm(request.GET)

    # Se o formulário for válido e contiver um valor de pesquisa
    # if form.is_valid() and form.cleaned_data.get('search'):
    #     search_term = form.cleaned_data['search']
    #     # Filtra os clientes pelo nome (ou outro campo desejado)
    #     clients = Person.objects.filter(id_FisicPerson_fk__name__icontains=search_term)
    # else:
    #     # Caso contrário, exibe todos os clientes
    clients = Person.objects.all()

    usuario_paginator = Paginator(clients,20)
    page_num = request.GET.get('page')
    page = usuario_paginator.get_page(page_num)
    print(page)
    return render(request, 'registry/client_list.html', { 'clients': page}) #'form': form,

@login_required
def buscar_clientes(request):
    """Busca clientes dinamicamente e retorna JSON."""
    query = request.GET.get('query', '')  # Recebe a entrada do usuário
    resultados = Person.objects.filter(
        Q(id__icontains=query) | 
        Q(id_FisicPerson_fk__name__icontains=query) | 
        Q(id_ForeignPerson_fk__name_foreigner__icontains=query) | 
        Q(id_LegalPerson_fk__fantasyName__icontains=query)
    ).order_by('id')[:20]  # Limita os resultados a 5

    if not resultados:
        return JsonResponse({'clientes': [], 'message': 'Nenhum cliente encontrado.'})

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
    return JsonResponse({'clientes': clients})
    # return render(request, 'registry/client_list.html', { 'clients': clients})

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

    return render(request, 'registry/Client_Get.html', {'client': client})
    return HttpResponse(client)

# @login_required
# def update_client(request, id_client):
#     client = get_object_or_404(Person, id=id_client)
#     fisicperson = client.id_FisicPerson_fk
#     legalperson = client.id_LegalPerson_fk
#     foreigner = client.id_ForeignPerson_fk
#     if fisicperson != None:
#         address = client.id_FisicPerson_fk.id_address_fk
#         print(address)
#     if legalperson != None:
#         address = client.id_LegalPerson_fk.id_address_fk
#         print(address)
#     if foreigner != None:
#         address = client.id_ForeignPerson_fk.id_address_fk
#         print(address)

#     client = get_object_or_404(Person, id=id_client)
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, instance=client)
#         if form.is_valid():
#             form.save()
#             return redirect('Product')
#     else:
#         form = ProductModelForm(instance=client)
#     return render(request, 'purchase/product_form.html', {'form': form})
    
#     pass



#     address = client.endereco  # Assume que cada cliente tem um endereço relacionado
#     fisic_person = client.pessoa_fisica  # Assume que cada cliente tem uma pessoa física relacionada

#     # Quando o formulário for enviado (POST)
#     if request.method == 'POST':
#         # Passa as instâncias para os subformulários
#         form = CombinedForm(request.POST, address_instance=address, fisic_person_instance=fisic_person, client_instance=client)

#         if form.is_valid():
#             # Salva os dados, cada subformulário cuida de salvar sua respectiva instância
#             form.save()  
#             return redirect('Client')  # Redireciona para a lista de clientes após a edição

#     else:
#         # No método GET, passamos as instâncias para carregar os dados
#         form = CombinedForm(address_instance=address, fisic_person_instance=fisic_person, client_instance=client)

#     return render(request, 'config/create_client_form.html', {'form': form})
