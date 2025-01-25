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
from django.http import JsonResponse, HttpResponse
### SUPPLIER - em breve desativado

# @login_required
# def supplier(request):
#     persons = Person.objects.all()
#     return render(request, 'purchase/supplier.html', {'persons': persons})

# @login_required
# def supplierForm(request):
#     if request.method == 'POST':
#         form = SupplierModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('Supplier')
#     else:
#         form = SupplierModelForm()
#     return render(request, 'purchase/supplierForm.html', {'form': form})

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
#     return render(request, 'purchase/supplierForm.html', {'form': form})

# @login_required
# def deleteSupplier(request, id_supplier):
#     person = get_object_or_404(Person, id=id_supplier)
#     if request.method == 'POST':
#         person.delete()
#         return redirect('Supplier')
#     return render(request, 'purchase/person_confirm_delete.html', {'person': person})


### PURCHASE

@login_required
def compras_list(request):
    compras = Compra.objects.all()
    return render(request, 'purchase/compras_list.html', {'compras': compras})

@login_required
def compras_create(request):
    # Configuração do formset para itens de compra e métodos de pagamento
    CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)
    PaymentMethodCompraFormSet = inlineformset_factory(Compra, PaymentMethod_Compra, form=PaymentMethodCompraForm, extra=1, can_delete=True)

    if request.method == 'POST':
        compra_form = CompraForm(request.POST)
        compra_item_formset = CompraItemFormSet(request.POST)
        payment_method_formset = PaymentMethodCompraFormSet(request.POST)

        if compra_form.is_valid() and compra_item_formset.is_valid() and payment_method_formset.is_valid():
            compra = compra_form.save()

            # A instância dos formsets de CompraItem e PaymentMethod_Compra é associada à nova instância de Compra
            compra_item_formset.instance = compra
            payment_method_formset.instance = compra

            # Salva os itens de compra (isso vai associar os CompraItem à compra)
            compra_item_formset.save()
            
            # Atualiza o estoque, adicionando a quantidade comprada
            for form in compra_item_formset:
                if form.cleaned_data:
                    produto = form.cleaned_data['produto']
                    quantidade = form.cleaned_data['quantidade']
                    preco_unitario = form.cleaned_data['preco_unitario']
                    
                    # Cria o item de compra
                    CompraItem.objects.create(
                        compra=compra,
                        produto=produto,
                        quantidade=quantidade,
                        preco_unitario=preco_unitario
                    )
                    
                    # Atualiza o estoque, somando a quantidade comprada
                    produto.current_quantity += quantidade
                    produto.save()

            # Salva as formas de pagamento associadas à compra
            payment_method_formset.save()
            
            return redirect('compras_list')
        
    else:
        compra_form = CompraForm()
        compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
        payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Compra.objects.none())
    
    context = {
        'compra_form': compra_form,
        'compra_item_formset': compra_item_formset,
        'payment_method_formset': payment_method_formset,
    }
    return render(request, 'purchase/compras_form.html', context)

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

    #             # Salva os itens da compra e adiciona ao estoque
    #             compra_item_formset.instance = compra
    #             compra_item_formset.save()
                
    #             for form in compra_item_formset:
    #                 if form.cleaned_data:
    #                     produto = form.cleaned_data['produto']
    #                     quantidade = form.cleaned_data['quantidade']
    #                     preco_unitario = form.cleaned_data['preco_unitario']
                        
    #                     # Cria o item de compra
    #                     CompraItem.objects.create(
    #                         compra=compra,
    #                         product=produto,
    #                         quantidade=quantidade,
    #                         preco_unitario=preco_unitario
    #                     )
                        
    #                     # Atualiza o estoque, adicionando a quantidade comprada
    #                     produto.current_quantity += quantidade
    #                     produto.save()

    #             # Salva as formas de pagamento associadas à compra
    #             payment_method_formset.instance = compra
    #             payment_method_formset.save()
                
    #             return redirect('compra_list')
            
    #     else:
    #         compra_form = CompraForm()
    #         compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
    #         payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Compra.objects.none())
        
    #     context = {
    #         'compra_form': compra_form,
    #         'compra_item_formset': compra_item_formset,
    #         'payment_method_formset': payment_method_formset
    #     }
    #     return render(request, 'purchase/compras_form.html', context)

@login_required
def compras_update(request, pk):
    # Recupera a instância da Compra existente
    compra = get_object_or_404(Compra, pk=pk)

    # Configuração do formset para itens de compra e métodos de pagamento
    CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)
    PaymentMethodCompraFormSet = inlineformset_factory(Compra, PaymentMethod_Compra, form=PaymentMethodCompraForm, extra=1, can_delete=True)

    if request.method == 'POST':
        # Recupera os dados do formulário de compra e formsets de itens e métodos de pagamento
        compra_form = CompraForm(request.POST, instance=compra)
        compra_item_formset = CompraItemFormSet(request.POST, instance=compra)
        payment_method_formset = PaymentMethodCompraFormSet(request.POST, instance=compra)

        if compra_form.is_valid() and compra_item_formset.is_valid() and payment_method_formset.is_valid():
            # Salva a compra (atualiza os dados da compra)
            compra = compra_form.save()

            # Atualiza os itens de compra
            compra_item_formset.save()

            # Atualiza o estoque, adicionando as quantidades compradas
            for form in compra_item_formset:
                if form.cleaned_data:
                    produto = form.cleaned_data['produto']
                    quantidade = form.cleaned_data['quantidade']

                    # Atualiza o estoque, somando a quantidade comprada
                    produto.current_quantity += quantidade
                    produto.save()

            # Salva as formas de pagamento associadas à compra
            payment_method_formset.save()

            # Redireciona para a lista de compras após a atualização
            return redirect('compras_list')

    else:
        # Se for um GET, inicializa o formulário com os dados da compra existente
        compra_form = CompraForm(instance=compra)
        compra_item_formset = CompraItemFormSet(queryset=compra.compraitem_set.all(), instance=compra)
        payment_method_formset = PaymentMethodCompraFormSet(queryset=compra.paymentmethod_compra_set.all(), instance=compra)

    context = {
        'compra_form': compra_form,
        'compra_item_formset': compra_item_formset,
        'payment_method_formset': payment_method_formset,
    }
    return render(request, 'purchase/compras_form.html', context)

    # def compras_update(request, pk):
    #     compra = get_object_or_404(Compra, pk=pk)
    #     CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)

    #     if request.method == 'POST':
    #         compra_form = CompraForm(request.POST, instance=compra)
    #         compra_item_formset = CompraItemFormSet(request.POST, instance=compra)

    #         if compra_form.is_valid() and compra_item_formset.is_valid():
    #             compra_form.save()
    #             compra_item_formset.save()
    #             return redirect('compra_list')

    #     else:
    #         compra_form = CompraForm(instance=compra)
    #         compra_item_formset = CompraItemFormSet(instance=compra)

    #     context = {
    #         'compra_form': compra_form,
    #         'compra_item_formset': compra_item_formset,
    #         'compra': compra,
    #     }

@login_required# Deletar uma Compra
def compras_delete(request, pk):
    # Obtém o objeto Compra ou retorna 404 se não encontrado
    compra = get_object_or_404(Compra, pk=pk)
    # Obtém todos os itens associados à compra
    compra_items = CompraItem.objects.filter(compra=compra)
    
    # Restaura a quantidade dos produtos no estoque
    for item in compra_items:
        produto = item.produto
        # Incrementa a quantidade de produto no estoque com a quantidade do item de compra
        produto.current_quantity += item.quantidade
        produto.save()
    
    # Deleta os itens de compra e a compra em si
    compra_items.delete()
    compra.delete()
    
    # Redireciona para a lista de compras
    return redirect('compras_list')

@login_required# Criar CompraItem para uma compra específica
def compras_item_create(request, compra_pk):
    # Obtém a compra específica à qual o item será adicionado
    compra = get_object_or_404(Compra, pk=compra_pk)

    if request.method == 'POST':
        form = CompraItemForm(request.POST)
        
        if form.is_valid():
            compra_item = form.save(commit=False)
            compra_item.compra = compra  # Associa o item à compra atual

            # Atualiza o estoque do produto
            produto = compra_item.produto
            if compra_item.quantidade > 0:
                produto.current_quantity += compra_item.quantidade
                produto.save()
            
            compra_item.save()  # Salva o item da compra no banco de dados
            messages.success(request, "Item adicionado à compra com sucesso!")
            return redirect('compra_detail', pk=compra.pk)  # Redireciona para a página de detalhes da compra
        else:
            messages.error(request, "Erro ao adicionar o item. Verifique os dados.")
    else:
        form = CompraItemForm()

    context = {
        'form': form,
        'compra': compra
    }
    return render(request, 'compras/compra_item_form.html', context) 

### PRODUCT

@login_required
def product(request):
    products = Product.objects.all()
    return render(request, 'purchase/product_list.html', {'products': products})

@login_required
def productForm(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Product')
    else:
        form = ProductModelForm()
    return render(request, 'purchase/product_form.html', {'form': form})

@login_required
def updateProduct(request, id_product):
    product = get_object_or_404(Product, id=id_product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('Product')
    else:
        form = ProductModelForm(instance=product)
    return render(request, 'purchase/product_form.html', {'form': form})

@login_required
def deleteProduct(request, id_product):
    product = get_object_or_404(Product, id=id_product)
    product.delete()
    return redirect('Product')

@login_required
def buscar_produtos(request):
    query = request.GET.get('query','').strip()
    page_num = request.GET.get('page',1)

    resultados = Product.objects.filter(
        Q(id__istartswith=query) |
        Q(description__istartswith=query) |
        Q(product_code__istartswith=query)
    ).order_by('id')

    products = [
        {
            'id':produto.id,
            'description':produto.description,
            'product_code': produto.product_code,
            'selling_price':produto.selling_price
        } for produto in resultados
    ]

    usuario_paginator = Paginator(products,20)
    page = usuario_paginator.get_page(page_num)

    response_data = {
        'produtos':list(page.object_list),
        'pagination':{
            'has_previous': page.has_previous(),
            'previous_page': page.previous_page_number() if page.has_previous() else None,
            'has_next': page.has_next(),
            'next_page': page.next_page_number() if page.has_next() else None,
            'current_page': page.number,
            'total_pages': usuario_paginator.num_pages,
        },
        'message': f"{len(products)} produtos encontrados" if page.object_list else "Nenhum produto encontrado."
    }

    return JsonResponse(response_data)