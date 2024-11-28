from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *

# ### CLIENT

@login_required
def create_client(request):
    if request.method == 'POST':
        form = CombinedForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o endereço, pessoa física e cliente
            return redirect('Client')  # Redireciona para a lista de clientes, ou página de sucesso
    else:
        form = CombinedForm()

    return render(request, 'config/create_client_form.html', {'form': form})

@login_required
def client_list(request):
    # Cria o formulário de pesquisa
    form = ClientSearchForm(request.GET)

    # Se o formulário for válido e contiver um valor de pesquisa
    if form.is_valid() and form.cleaned_data.get('search'):
        search_term = form.cleaned_data['search']
        # Filtra os clientes pelo nome (ou outro campo desejado)
        clients = Client.objects.filter(pessoa_fisica__name__icontains=search_term)
    else:
        # Caso contrário, exibe todos os clientes
        clients = Client.objects.all()

    return render(request, 'config/client_list.html', {'form': form, 'clients': clients})

@login_required
def update_client(request, id_client):
    client = get_object_or_404(Client, id=id_client)
    address = client.endereco  # Assume que cada cliente tem um endereço relacionado
    fisic_person = client.pessoa_fisica  # Assume que cada cliente tem uma pessoa física relacionada

    # Quando o formulário for enviado (POST)
    if request.method == 'POST':
        # Passa as instâncias para os subformulários
        form = CombinedForm(request.POST, address_instance=address, fisic_person_instance=fisic_person, client_instance=client)

        if form.is_valid():
            # Salva os dados, cada subformulário cuida de salvar sua respectiva instância
            form.save()  
            return redirect('Client')  # Redireciona para a lista de clientes após a edição

    else:
        # No método GET, passamos as instâncias para carregar os dados
        form = CombinedForm(address_instance=address, fisic_person_instance=fisic_person, client_instance=client)

    return render(request, 'config/create_client_form.html', {'form': form})

@login_required
def delete_client(request, id_client):
    # Recupera o cliente com o id fornecido
    client = get_object_or_404(Client, id=id_client)
    client.delete()
    return redirect('Client')
