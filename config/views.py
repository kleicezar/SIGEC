from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *

def index(request):
    return render(request, 'config/index.html')

### PAYMENT METHOD

def paymentMethod(request):
    context = {
        'PaymentMethods': PaymentMethod.objects.all()
    }
    return render(request, 'config/PaymentMethod.html', context)

def PaymentMethodForm(request):
    if request.method == "GET":
        paymentMethodForm = PaymentMethodModelForm()
        context = {
            'paymentMethod' : paymentMethodForm
        }
        return render(request, 'config/PaymentMethodForm.html', context)
    else:
        paymentMethodForm = PaymentMethodModelForm(request.POST)
        if paymentMethodForm.is_valid():
            paymentMethodForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('PaymentMethod')
    context = {
        'paymentMethod' : paymentMethodForm
    }
    return render(request, 'config/PaymentMethod.html', context)
    
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

def position(request):
    context = {
        'Positions': Position.objects.all()
    }
    return render(request, 'config/Position.html', context)

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

def situation(request):
    context = {
        'Situations': Situation.objects.all()
    }
    return render(request, 'config/Situation.html', context)

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
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('Situation')
    context = {
        'Situation' : situationForm
    }
    return render(request, 'config/Situation.html', context)

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
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('Situation')
    context = {
        'Situation' : situationForm
    }
    return render(request, 'config/Situation.html', context)

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

### SUPPLIER

def supplier(request):
    persons = Person.objects.all()
    return render(request, 'config/supplier.html', {'persons': persons})

def supplierForm(request):
    if request.method == 'POST':
        form = SupplierModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Supplier')
    else:
        form = SupplierModelForm()
    return render(request, 'config/supplierForm.html', {'form': form})

def updateSupplier(request, id_supplier):
    person = get_object_or_404(Person, id=id_supplier)
    if request.method == 'POST':
        form = SupplierModelForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('Supplier')
    else:
        form = SupplierModelForm(instance=person)
    return render(request, 'config/supplierForm.html', {'form': form})

def deleteSupplier(request, id_supplier):
    person = get_object_or_404(Person, id=id_supplier)
    if request.method == 'POST':
        person.delete()
        return redirect('Supplier')
    return render(request, 'config/person_confirm_delete.html', {'person': person})

### PRODUCT

def product(request):
    products = Product.objects.all()
    return render(request, 'config/product_list.html', {'products': products})

def productForm(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Product')
    else:
        form = ProductModelForm()
    return render(request, 'config/product_form.html', {'form': form})

def updateProduct(request, id_product):
    product = get_object_or_404(Product, id=id_product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('Product')
    else:
        form = ProductModelForm(instance=product)
    return render(request, 'config/product_form.html', {'form': form})

def deleteProduct(request, id_product):
    product = get_object_or_404(Product, id=id_product)
    if request.method == 'POST':
        product.delete()
        return redirect('Product')
    return render(request, 'config/product_confirm_delete.html', {'product': product})

### CLIENT

def create_client(request):
    if request.method == 'POST':
        form = CombinedForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o endereço, pessoa física e cliente
            return redirect('Client')  # Redireciona para a lista de clientes, ou página de sucesso
    else:
        form = CombinedForm()

    return render(request, 'config/create_client_form.html', {'form': form})

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

def delete_client(request, id_client):
    # Recupera o cliente com o id fornecido
    client = get_object_or_404(Client, id=id_client)

    # Deleta o cliente
    client.delete()

    # Redireciona para a lista de clientes após a exclusão
    return redirect('Client')

### SALE

def venda_list(request):
    vendas = Venda.objects.all()
    return render(request, 'config/venda_list.html', {'vendas': vendas})

# Criar uma nova Venda
# def venda_create(request):
#     if request.method == 'POST':
#         form = VendaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('venda_list')  # Redireciona para a lista de vendas
#     else:
#         form = VendaForm()
#     return render(request, 'config/venda_form.html', {'form': form})


# Criar uma nova Venda com itens
# def venda_create(request):
#     if request.method == 'POST':
#         venda_form = VendaForm(request.POST)
#         # Como o formulário de VendaItem precisa ser adicionado de forma dinâmica, vamos criar uma instância dele manualmente
#         venda_items = [VendaItemForm(request.POST, prefix=f"item_{i}") for i in range(1)]  # Inicia com 5 campos de item (ajuste conforme necessário)

#         if venda_form.is_valid():
#             venda = venda_form.save()

#             # Salvando os itens da venda
#             for item_form in venda_items:
#                 if item_form.is_valid():
#                     venda_item = item_form.save(commit=False)
#                     venda_item.venda = venda
#                     venda_item.save()

#             return redirect('venda_list')  # Redireciona para a lista de vendas
#     else:
#         venda_form = VendaForm()
#         venda_items = [VendaItemForm(prefix=f"item_{i}") for i in range(1)]  # Campos iniciais

#     return render(request, 'config/venda_form.html', {'venda_form': venda_form, 'venda_items': venda_items})

# def venda_create(request):
#     if request.method == 'POST':
#         venda_form = VendaForm(request.POST)
#         venda_items = [VendaItemForm(request.POST, prefix=f"item_{i}") for i in range(1)] 

#         if venda_form.is_valid():
#             venda = venda_form.save()

#             for item_form in venda_items:
#                 if item_form.is_valid():
#                     venda_item = item_form.save(commit=False)
#                     venda_item.venda = venda
#                     venda_item.save()

#             return redirect('venda_list')  
#     else:
#         venda_form = VendaForm()
#         venda_items = [VendaItemForm(prefix=f"item_{i}") for i in range(1)]  
#         products = Product.objects.all()  # Obtendo todos os produtos

#     return render(request, 'config/venda_form.html', {
#         'venda_form': venda_form, 
#         'venda_items': venda_items, 
#         'products': products  # Passando os produtos ao template
#     })

def venda_create(request):
    if request.method == 'POST':
        venda_form = VendaForm(request.POST)
        venda_items = [VendaItemForm(request.POST, prefix=f"item_{i}") for i in range(2)] 

        if venda_form.is_valid():
            venda = venda_form.save()

            for item_form in venda_items:
                if item_form.is_valid():
                    venda_item = item_form.save(commit=False)
                    venda_item.venda = venda
                    venda_item.save()

            return redirect('venda_list')  
    else:
        venda_form = VendaForm()
        venda_items = [VendaItemForm(prefix=f"item_{i}") for i in range(2)]  
        products = Product.objects.all()  # Obtendo todos os produtos

    return render(request, 'config/venda_form.html', {
        'venda_form': venda_form, 
        'venda_items': venda_items, 
        'products': products  # Passando os produtos ao template
    })

# Editar uma Venda existente
def venda_update(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if request.method == 'POST':
        form = VendaForm(request.POST, instance=venda)
        if form.is_valid():
            form.save()
            return redirect('venda_list')  # Redireciona para a lista de vendas
    else:
        form = VendaForm(instance=venda)
    return render(request, 'config/venda_form.html', {'form': form})

# Deletar uma Venda
def venda_delete(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    if request.method == 'POST':
        venda.delete()
        return redirect('venda_list')  # Redireciona para a lista de vendas
    return render(request, 'config/venda_confirm_delete.html', {'venda': venda})

# Criar VendaItem para uma venda específica
def venda_item_create(request, venda_pk):
    venda = get_object_or_404(Venda, pk=venda_pk)
    if request.method == 'POST':
        form = VendaItemForm(request.POST)
        if form.is_valid():
            venda_item = form.save(commit=False)
            venda_item.venda = venda
            venda_item.save()
            return redirect('venda_detail', pk=venda.pk)  # Redireciona para os detalhes da venda
    else:
        form = VendaItemForm()
    return render(request, 'config/venda_item_form.html', {'form': form, 'venda': venda})