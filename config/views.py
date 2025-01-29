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

### PAYMENT METHOD
@login_required
def paymentMethod(request):
    context = {
        'PaymentMethods': PaymentMethod.objects.all()
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required
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

@login_required    
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

@login_required
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
@login_required
def position(request):
    context = {
        'Positions': Position.objects.all()
    }
    return render(request, 'config/Position.html', context)


@login_required
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

@login_required
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

@login_required
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

@login_required
def situation(request):
    context = {
        'Situations': Situation.objects.all()
    }
    return render(request, 'config/Situation.html', context)

@login_required
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

@login_required
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

@login_required
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

### ChartOfAccounts

@login_required
def chartOfAccounts(request):
    context = {
        'ChartOfAccounts': ChartOfAccounts.objects.all()
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
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
            messages.success(request, "Plano de Contas cadastrado com sucesso")
            return redirect('ChartOfAccounts')
        else:
            print('Erros:',chartOfAccountsForm.errors)
    context = {
        'ChartOfAccounts' : chartOfAccountsForm
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
def updateChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "GET":
        chartOfAccountsForm = ChartOfAccountsModelForm(instance=chartOfAccounts)

        context = {
            'chartOfAccounts': chartOfAccounts,
            'ChartOfAccounts': chartOfAccountsForm
        }
        return render(request, 'config/ChartOfAccountsForm.html',context)
    elif request.method == "POST":
        chartOfAccountsForm = ChartOfAccountsModelForm(request.POST, instance=chartOfAccounts)
        if chartOfAccountsForm.is_valid():
            chartOfAccountsForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('ChartOfAccounts')
    context = {
        'ChartOfAccounts' : chartOfAccountsForm
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
def deleteChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "POST":
        chartOfAccounts.delete()
        messages.success(request, "Situação deletada com sucesso.")
        return redirect('ChartOfAccounts')  # Redirecione para onde desejar
    context = {
        'chartOfAccounts': chartOfAccounts
    }

    return render(request, 'config/ChartOfAccounts.html', context)

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
# name_paymentMethod = models.CharField('Nome da Forma de Pagamento', max_length=50)
    # is_Active = models.BooleanField('ativo')
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
    # @login_required
# def index(request):
#     return render(request, 'config/index.html')

# ### SUPPLIER

# @login_required
# def supplier(request):
#     persons = Person.objects.all()
#     return render(request, 'config/supplier.html', {'persons': persons})

# @login_required
# def supplierForm(request):
#     if request.method == 'POST':
#         form = SupplierModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('Supplier')
#     else:
#         form = SupplierModelForm()
#     return render(request, 'config/supplierForm.html', {'form': form})

# @login_required
# def updateSupplier(request, id_supplier):
#     person = get_object_or_404(Person, id=id_supplier)
#     if request.method == 'POST':
#         form = SupplierModelForm(request.POST, instance=person)
#         if form.is_valid():
#             form.save()
#             return redirect('Supplier')
#     else:
#         form = SupplierModelForm(instance=person)
#     return render(request, 'config/supplierForm.html', {'form': form})

# @login_required
# def deleteSupplier(request, id_supplier):
#     person = get_object_or_404(Person, id=id_supplier)
#     if request.method == 'POST':
#         person.delete()
#         return redirect('Supplier')
#     return render(request, 'config/person_confirm_delete.html', {'person': person})

# ### PRODUCT

# @login_required
# def product(request):
#     products = Product.objects.all()
#     return render(request, 'config/product_list.html', {'products': products})

# @login_required
# def productForm(request):
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('Product')
#     else:
#         form = ProductModelForm()
#     return render(request, 'config/product_form.html', {'form': form})

# @login_required
# def updateProduct(request, id_product):
#     product = get_object_or_404(Product, id=id_product)
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('Product')
#     else:
#         form = ProductModelForm(instance=product)
#     return render(request, 'config/product_form.html', {'form': form})

# @login_required
# def deleteProduct(request, id_product):
#     product = get_object_or_404(Product, id=id_product)
#     product.delete()
#     return redirect('Product')

    # ### CLIENT

    # @login_required
    # def create_client(request):
    #     if request.method == 'POST':
    #         form = CombinedForm(request.POST)
    #         if form.is_valid():
    #             form.save()  # Salva o endereço, pessoa física e cliente
    #             return redirect('Client')  # Redireciona para a lista de clientes, ou página de sucesso
    #     else:
    #         form = CombinedForm()

    #     return render(request, 'config/create_client_form.html', {'form': form})

    # @login_required
    # def client_list(request):
    #     # Cria o formulário de pesquisa
    #     form = ClientSearchForm(request.GET)

    #     # Se o formulário for válido e contiver um valor de pesquisa
    #     if form.is_valid() and form.cleaned_data.get('search'):
    #         search_term = form.cleaned_data['search']
    #         # Filtra os clientes pelo nome (ou outro campo desejado)
    #         clients = Client.objects.filter(pessoa_fisica__name__icontains=search_term)
    #     else:
    #         # Caso contrário, exibe todos os clientes
    #         clients = Client.objects.all()

    #     return render(request, 'config/client_list.html', {'form': form, 'clients': clients})

    # @login_required
    # def update_client(request, id_client):
    #     client = get_object_or_404(Client, id=id_client)
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

    # @login_required
    # def delete_client(request, id_client):
    #     # Recupera o cliente com o id fornecido
    #     client = get_object_or_404(Client, id=id_client)
    #     client.delete()
    #     return redirect('Client')

# ### SALE

# @login_required
# def venda_list(request):
#     vendas = Venda.objects.all()
#     return render(request, 'config/venda_list.html', {'vendas': vendas})

#     # 
#     # @login_requiredCriar uma nova Venda
#     # def venda_create(request):
#     #     if request.method == 'POST':
#     #         form = VendaForm(request.POST)
#     #         if form.is_valid():
#     #             form.save()
#     #             return redirect('venda_list')  # Redireciona para a lista de vendas
#     #     else:
#     #         form = VendaForm()
#     #     return render(request, 'config/venda_form.html', {'form': form})


#     # 
#     # @login_requiredCriar uma nova Venda com itens
#     # def venda_create(request):
#     #     if request.method == 'POST':
#     #         venda_form = VendaForm(request.POST)
#     #         # Como o formulário de VendaItem precisa ser adicionado de forma dinâmica, vamos criar uma instância dele manualmente
#     #         venda_items = [VendaItemForm(request.POST, prefix=f"item_{i}") for i in range(1)]  # Inicia com 5 campos de item (ajuste conforme necessário)

#     #         if venda_form.is_valid():
#     #             venda = venda_form.save()

#     #             # Salvando os itens da venda
#     #             for item_form in venda_items:
#     #                 if item_form.is_valid():
#     #                     venda_item = item_form.save(commit=False)
#     #                     venda_item.venda = venda
#     #                     venda_item.save()

#     #             return redirect('venda_list')  # Redireciona para a lista de vendas
#     #     else:
#     #         venda_form = VendaForm()
#     #         venda_items = [VendaItemForm(prefix=f"item_{i}") for i in range(1)]  # Campos iniciais

#     #     return render(request, 'config/venda_form.html', {'venda_form': venda_form, 'venda_items': venda_items})

# @login_required
# def venda_create(request):
#     VendaItemFormSet = inlineformset_factory(Venda, VendaItem, form=VendaItemForm, extra=1, can_delete=True)
#     PaymentMethodVendaFormSet = inlineformset_factory(Venda, PaymentMethod_Venda, form=PaymentMethodVendaForm, extra=1, can_delete=True)
#     # VendaItemFormSet = modelformset_factory(VendaItem, form=VendaItemForm, extra=1)
#     # PaymentMethodVendaFormSet = modelformset_factory(PaymentMethod_Venda, form=PaymentMethodVendaForm, extra=1)
    
#     if request.method == 'POST':
#         venda_form = VendaForm(request.POST)
#         venda_item_formset = VendaItemFormSet(request.POST)
#         payment_method_formset = PaymentMethodVendaFormSet(request.POST)
        
#         if venda_form.is_valid() and venda_item_formset.is_valid() and payment_method_formset.is_valid():
#             estoque_suficiente = True
#             for form in venda_item_formset:
#                 if form.cleaned_data:
#                     produto = form.cleaned_data['product']
#                     quantidade = form.cleaned_data['quantidade']
#                     if produto.current_quantity < quantidade:
#                         estoque_suficiente = False
#                         form.add_error('quantidade', f'Não há estoque suficiente para o produto {produto.description}. Estoque disponível: {produto.current_quantity}.')

#             if estoque_suficiente:
#                 venda = venda_form.save()

#                 venda_item_formset.instance = venda
#                 venda_item_formset.save()
                
#                 # Salva os itens da venda
#                 for form in venda_item_formset:
#                     if form.cleaned_data:
#                         produto = form.cleaned_data['product']
#                         quantidade = form.cleaned_data['quantidade']
#                         preco_unitario = form.cleaned_data['preco_unitario']
                        
#                         VendaItem.objects.create(
#                             venda=venda,
#                             product=produto,
#                             quantidade=quantidade,
#                             preco_unitario=preco_unitario
#                         )
                        
#                         produto.current_quantity -= quantidade
#                         produto.save()

#                 # Salva as formas de pagamento associadas à venda
#                 for form in payment_method_formset:
#                     if form.cleaned_data:
#                         forma_pagamento = form.cleaned_data['forma_pagamento']
#                         expiration_date = form.cleaned_data['expirationDate']
#                         valor = form.cleaned_data['valor']
                        
#                         PaymentMethod_Venda.objects.create(
#                             venda=venda,
#                             forma_pagamento=forma_pagamento,
#                             expirationDate=expiration_date,
#                             valor=valor
#                         )
                
#                 return redirect('venda_list')
        
#     else:
#         venda_form = VendaForm()
#         venda_item_formset = VendaItemFormSet(queryset=VendaItem.objects.none())
#         payment_method_formset = PaymentMethodVendaFormSet(queryset=PaymentMethod_Venda.objects.none())
#     context = {
#         'venda_form': venda_form,   
#         'venda_item_formset': venda_item_formset,
#         'payment_method_formset': payment_method_formset
#     }
#     return render(request, 'config/venda_form.html', context)

# @login_required
# def venda_update(request, pk):
#     # Carregar a venda existente
#     venda = get_object_or_404(Venda, pk=pk)

#     # Criar formsets para itens de venda e formas de pagamento
#     VendaItemFormSet = inlineformset_factory(Venda, VendaItem, form=VendaItemForm, extra=1, can_delete=True)
#     PaymentMethodVendaFormSet = inlineformset_factory(Venda, PaymentMethod_Venda, form=PaymentMethodVendaForm, extra=1, can_delete=True)

#     if request.method == 'POST':
#         venda_form = VendaForm(request.POST, instance=venda)
#         venda_item_formset = VendaItemFormSet(request.POST, instance=venda)
#         payment_method_formset = PaymentMethodVendaFormSet(request.POST, instance=venda)

#         if venda_form.is_valid() and venda_item_formset.is_valid() and payment_method_formset.is_valid():
#             # Salvar a venda
#             venda_form.save()
#             venda_item_formset.save()
#             payment_method_formset.save()

#             messages.success(request, "Venda atualizada com sucesso!")
#             return redirect('venda_list')

#         else:
#             messages.error(request, "Erro ao atualizar a venda. Verifique os campos.")

#     else:
#         venda_form = VendaForm(instance=venda)
#         venda_item_formset = VendaItemFormSet(instance=venda)
#         payment_method_formset = PaymentMethodVendaFormSet(instance=venda)

#     context = {
#         'venda_form': venda_form,
#         'venda_item_formset': venda_item_formset,
#         'payment_method_formset': payment_method_formset,
#         'venda': venda,
#     }

#     return render(request, 'config/venda_form.html', context)

# @login_required# Deletar uma Venda
# def venda_delete(request, pk):
#     # Obtém a venda com base no id (pk)
#     venda = get_object_or_404(Venda, pk=pk)
#     # Recupera os itens de venda relacionados
#     venda_items = VendaItem.objects.filter(venda=venda)
#     # Restaura a quantidade dos produtos no estoque
#     for item in venda_items:
#         produto = item.product
#         produto.current_quantity += item.quantidade  # Restaura a quantidade
#         produto.save()
#     # Exclui os itens de venda
#     venda_items.delete()
#     # Exclui a venda
#     venda.delete()
#     # Redireciona para a lista de vendas após a deleção
#     return redirect('venda_list')

# @login_required# Criar VendaItem para uma venda específica
# def venda_item_create(request, venda_pk):
#     venda = get_object_or_404(Venda, pk=venda_pk)
#     if request.method == 'POST':
#         form = VendaItemForm(request.POST)
#         if form.is_valid():
#             venda_item = form.save(commit=False)
#             venda_item.venda = venda
#             venda_item.save()
#             return redirect('venda_detail', pk=venda.pk)  # Redireciona para os detalhes da venda
#     else:
#         form = VendaItemForm()
#     return render(request, 'config/venda_item_form.html', {'form': form, 'venda': venda})

# @login_required
# def compras_list(request)

# @login_required
# def compras_list(request):
#     compras = Compra.objects.all()
#     return render(request, 'config/compras_list.html', {'compras': compras})

# @login_required
# def compras_create(request):
#     # Configuração do formset para itens de compra e métodos de pagamento
#     CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)
#     PaymentMethodCompraFormSet = inlineformset_factory(Compra, PaymentMethod_Compra, form=PaymentMethodCompraForm, extra=1, can_delete=True)

#     if request.method == 'POST':
#         compra_form = CompraForm(request.POST)
#         compra_item_formset = CompraItemFormSet(request.POST)
#         payment_method_formset = PaymentMethodCompraFormSet(request.POST)

#         if compra_form.is_valid() and compra_item_formset.is_valid() and payment_method_formset.is_valid():
#             compra = compra_form.save()

#             # A instância dos formsets de CompraItem e PaymentMethod_Compra é associada à nova instância de Compra
#             compra_item_formset.instance = compra
#             payment_method_formset.instance = compra

#             # Salva os itens de compra (isso vai associar os CompraItem à compra)
#             compra_item_formset.save()
            
#             # Atualiza o estoque, adicionando a quantidade comprada
#             for form in compra_item_formset:
#                 if form.cleaned_data:
#                     produto = form.cleaned_data['produto']
#                     quantidade = form.cleaned_data['quantidade']
#                     preco_unitario = form.cleaned_data['preco_unitario']
                    
#                     # Cria o item de compra
#                     CompraItem.objects.create(
#                         compra=compra,
#                         produto=produto,
#                         quantidade=quantidade,
#                         preco_unitario=preco_unitario
#                     )
                    
#                     # Atualiza o estoque, somando a quantidade comprada
#                     produto.current_quantity += quantidade
#                     produto.save()

#             # Salva as formas de pagamento associadas à compra
#             payment_method_formset.save()
            
#             return redirect('compras_list')
        
#     else:
#         compra_form = CompraForm()
#         compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
#         payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Compra.objects.none())
    
#     context = {
#         'compra_form': compra_form,
#         'compra_item_formset': compra_item_formset,
#         'payment_method_formset': payment_method_formset,
#     }
#     return render(request, 'config/compras_form.html', context)

#     # def compras_create(request):
#     #     # Configuração do formset para itens de compra e métodos de pagamento
#     #     CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)
#     #     PaymentMethodCompraFormSet = inlineformset_factory(Compra, PaymentMethod_Compra, form=PaymentMethodCompraForm, extra=1, can_delete=True)

#     #     if request.method == 'POST':
#     #         compra_form = CompraForm(request.POST)
#     #         compra_item_formset = CompraItemFormSet(request.POST)
#     #         payment_method_formset = PaymentMethodCompraFormSet(request.POST)

#     #         if compra_form.is_valid() and compra_item_formset.is_valid() and payment_method_formset.is_valid():
#     #             compra = compra_form.save()

#     #             # Salva os itens da compra e adiciona ao estoque
#     #             compra_item_formset.instance = compra
#     #             compra_item_formset.save()
                
#     #             for form in compra_item_formset:
#     #                 if form.cleaned_data:
#     #                     produto = form.cleaned_data['produto']
#     #                     quantidade = form.cleaned_data['quantidade']
#     #                     preco_unitario = form.cleaned_data['preco_unitario']
                        
#     #                     # Cria o item de compra
#     #                     CompraItem.objects.create(
#     #                         compra=compra,
#     #                         product=produto,
#     #                         quantidade=quantidade,
#     #                         preco_unitario=preco_unitario
#     #                     )
                        
#     #                     # Atualiza o estoque, adicionando a quantidade comprada
#     #                     produto.current_quantity += quantidade
#     #                     produto.save()

#     #             # Salva as formas de pagamento associadas à compra
#     #             payment_method_formset.instance = compra
#     #             payment_method_formset.save()
                
#     #             return redirect('compra_list')
            
#     #     else:
#     #         compra_form = CompraForm()
#     #         compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
#     #         payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Compra.objects.none())
        
#     #     context = {
#     #         'compra_form': compra_form,
#     #         'compra_item_formset': compra_item_formset,
#     #         'payment_method_formset': payment_method_formset
#     #     }
#     #     return render(request, 'config/compras_form.html', context)

# @login_required
# def compras_update(request, pk):
#     # Recupera a instância da Compra existente
#     compra = get_object_or_404(Compra, pk=pk)

#     # Configuração do formset para itens de compra e métodos de pagamento
#     CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)
#     PaymentMethodCompraFormSet = inlineformset_factory(Compra, PaymentMethod_Compra, form=PaymentMethodCompraForm, extra=1, can_delete=True)

#     if request.method == 'POST':
#         # Recupera os dados do formulário de compra e formsets de itens e métodos de pagamento
#         compra_form = CompraForm(request.POST, instance=compra)
#         compra_item_formset = CompraItemFormSet(request.POST, instance=compra)
#         payment_method_formset = PaymentMethodCompraFormSet(request.POST, instance=compra)

#         if compra_form.is_valid() and compra_item_formset.is_valid() and payment_method_formset.is_valid():
#             # Salva a compra (atualiza os dados da compra)
#             compra = compra_form.save()

#             # Atualiza os itens de compra
#             compra_item_formset.save()

#             # Atualiza o estoque, adicionando as quantidades compradas
#             for form in compra_item_formset:
#                 if form.cleaned_data:
#                     produto = form.cleaned_data['produto']
#                     quantidade = form.cleaned_data['quantidade']

#                     # Atualiza o estoque, somando a quantidade comprada
#                     produto.current_quantity += quantidade
#                     produto.save()

#             # Salva as formas de pagamento associadas à compra
#             payment_method_formset.save()

#             # Redireciona para a lista de compras após a atualização
#             return redirect('compras_list')

#     else:
#         # Se for um GET, inicializa o formulário com os dados da compra existente
#         compra_form = CompraForm(instance=compra)
#         compra_item_formset = CompraItemFormSet(queryset=compra.compraitem_set.all(), instance=compra)
#         payment_method_formset = PaymentMethodCompraFormSet(queryset=compra.paymentmethod_compra_set.all(), instance=compra)

#     context = {
#         'compra_form': compra_form,
#         'compra_item_formset': compra_item_formset,
#         'payment_method_formset': payment_method_formset,
#     }
#     return render(request, 'config/compras_form.html', context)

#     # def compras_update(request, pk):
#     #     compra = get_object_or_404(Compra, pk=pk)
#     #     CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)

#     #     if request.method == 'POST':
#     #         compra_form = CompraForm(request.POST, instance=compra)
#     #         compra_item_formset = CompraItemFormSet(request.POST, instance=compra)

#     #         if compra_form.is_valid() and compra_item_formset.is_valid():
#     #             compra_form.save()
#     #             compra_item_formset.save()
#     #             return redirect('compra_list')

#     #     else:
#     #         compra_form = CompraForm(instance=compra)
#     #         compra_item_formset = CompraItemFormSet(instance=compra)

#     #     context = {
#     #         'compra_form': compra_form,
#     #         'compra_item_formset': compra_item_formset,
#     #         'compra': compra,
#     #     }

# @login_required# Deletar uma Compra
# def compras_delete(request, pk):
#     # Obtém o objeto Compra ou retorna 404 se não encontrado
#     compra = get_object_or_404(Compra, pk=pk)
#     # Obtém todos os itens associados à compra
#     compra_items = CompraItem.objects.filter(compra=compra)
    
#     # Restaura a quantidade dos produtos no estoque
#     for item in compra_items:
#         produto = item.produto
#         # Incrementa a quantidade de produto no estoque com a quantidade do item de compra
#         produto.current_quantity += item.quantidade
#         produto.save()
    
#     # Deleta os itens de compra e a compra em si
#     compra_items.delete()
#     compra.delete()
    
#     # Redireciona para a lista de compras
#     return redirect('compras_list')

# @login_required# Criar CompraItem para uma compra específica
# def compras_item_create(request, compra_pk):
#     # Obtém a compra específica à qual o item será adicionado
#     compra = get_object_or_404(Compra, pk=compra_pk)

#     if request.method == 'POST':
#         form = CompraItemForm(request.POST)
        
#         if form.is_valid():
#             compra_item = form.save(commit=False)
#             compra_item.compra = compra  # Associa o item à compra atual

#             # Atualiza o estoque do produto
#             produto = compra_item.produto
#             if compra_item.quantidade > 0:
#                 produto.current_quantity += compra_item.quantidade
#                 produto.save()
            
#             compra_item.save()  # Salva o item da compra no banco de dados
#             messages.success(request, "Item adicionado à compra com sucesso!")
#             return redirect('compra_detail', pk=compra.pk)  # Redireciona para a página de detalhes da compra
#         else:
#             messages.error(request, "Erro ao adicionar o item. Verifique os dados.")
#     else:
#         form = CompraItemForm()

#     context = {
#         'form': form,
#         'compra': compra
#     }
#     return render(request, 'compras/compra_item_form.html', context) 

# def my_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#     return render(request, 'config/login.html')

# @login_required
# def my_logout(request):
#     logout(request)
#     return redirect('index') 