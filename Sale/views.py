from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
### SALE

@login_required
def venda_list(request):
    search_query = request.GET.get('query','')


    if search_query:
        sales = Venda.objects.filter(
        Q(id__istartswith=search_query) | 
        Q(pessoa__id_FisicPerson_fk__name__istartswith=search_query) |
        Q(pessoa__id_ForeignPerson_fk__name_foreigner__istartswith=search_query) |
        Q(pessoa__id_LegalPerson_fk__fantasyName__istartswith=search_query)
    ).order_by('id')
    else:
        sales = Venda.objects.all()

    paginator = Paginator(sales,1)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'sale/venda_list.html', {
        'vendas': page,
        'query':search_query
        })
@login_required
def venda_create(request):
    VendaItemFormSet = inlineformset_factory(Venda, VendaItem, form=VendaItemForm, extra=1, can_delete=True)
    PaymentMethodVendaFormSet = inlineformset_factory(Venda, PaymentMethod_Venda, form=PaymentMethodVendaForm, extra=1, can_delete=True)

    if request.method == 'POST':
        venda_form = VendaForm(request.POST)
        venda_item_formset = VendaItemFormSet(request.POST)
        print()
        payment_method_formset = PaymentMethodVendaFormSet(request.POST)
        # Percorrer VendaForm, manipular,

        if venda_form.is_valid() and venda_item_formset.is_valid() and payment_method_formset.is_valid():
            estoque_suficiente = True
            for form in venda_item_formset:
                if form.cleaned_data:
                    produto = form.cleaned_data['product']
                    quantidade = form.cleaned_data['quantidade']
                    if produto.current_quantity < quantidade:
                        estoque_suficiente = False
                        form.add_error('quantidade', f'Não há estoque suficiente para o produto {produto.description}. Estoque disponível: {produto.current_quantity}.')

            if estoque_suficiente:
                venda = venda_form.save()

                for form in venda_item_formset:
                    if form.cleaned_data:
                        produto = form.cleaned_data['product']
                        quantidade = form.cleaned_data['quantidade']
                        preco_unitario = form.cleaned_data['preco_unitario']
                        discount = form.cleaned_data['discount']
                        price_total = form.cleaned_data['price_total']
                        if not form.cleaned_data.get("DELETE"):
                            VendaItem.objects.create(
                                venda=venda,
                                product=produto,
                                quantidade=quantidade,
                                preco_unitario=preco_unitario,
                                discount = discount,
                                price_total = price_total
                            )
                            
                            produto.current_quantity -= quantidade
                            produto.save()
                        
                payment_method_formset.instance = venda
                total_payment = 0
                for form in payment_method_formset: 
                    if form.cleaned_data:
                        valor = form.cleaned_data['valor']
                        total_payment+=valor
                if(total_payment == venda_form.cleaned_data['total_value']):  
                    payment_method_formset.save()
                    for form in payment_method_formset.deleted_objects:
                        form.delete()
                        form.save()
                else:
                    messages.warning(request, "Ação cancelada! O valor não foi salvo completamente.")
                    venda_form = VendaForm()
                    venda_item_formset = VendaItemFormSet(queryset=VendaItem.objects.none())
                    payment_method_formset = PaymentMethodVendaFormSet(queryset=PaymentMethod_Venda.objects.none())
                    context = {
                        'venda_form': venda_form,       
                        'venda_item_formset': venda_item_formset,
                        'payment_method_formset': payment_method_formset
                    }
                    return render(request, 'sale/venda_form.html', context)
                return redirect('venda_list')
    else:
        venda_form = VendaForm()
        venda_item_formset = VendaItemFormSet(queryset=VendaItem.objects.none())
        payment_method_formset = PaymentMethodVendaFormSet(queryset=PaymentMethod_Venda.objects.none())
    context = {
        'venda_form': venda_form,       
        'venda_item_formset': venda_item_formset,
        'payment_method_formset': payment_method_formset
    }
    return render(request, 'sale/venda_form.html', context)

@login_required
def venda_update(request, pk):
    # Carregar a venda existente
    venda = get_object_or_404(Venda, pk=pk)

    # Criar formsets para itens de venda e formas de pagamento
    VendaItemFormSet = inlineformset_factory(Venda, VendaItem, form=VendaItemForm, extra=1, can_delete=True)
    PaymentMethodVendaFormSet = inlineformset_factory(Venda, PaymentMethod_Venda, form=PaymentMethodVendaForm, extra=1, can_delete=True)

    if request.method == 'POST':
        venda_form = VendaForm(request.POST, instance=venda)
        venda_item_formset = VendaItemFormSet(request.POST, instance=venda)
        payment_method_formset = PaymentMethodVendaFormSet(request.POST, instance=venda)

        if venda_form.is_valid() and venda_item_formset.is_valid() and payment_method_formset.is_valid():
            # Salvar a venda
            venda_form.save()
            venda_item_formset.save()
            payment_method_formset.save()

            messages.success(request, "Venda atualizada com sucesso!")
            return redirect('venda_list')
        if not venda_form.is_valid():
            print('Erros no venda_form: ',venda_form.errors)
        elif not venda_item_formset.is_valid():
            print('Erros no venda_item_formset',venda_item_formset.errors)
        elif not payment_method_formset.is_valid():
            print('Erros no payment_method_formset',payment_method_formset.errors)
        else:
            messages.error(request, "Erro ao atualizar a venda. Verifique os campos.")

    else:
        venda_form = VendaForm(instance=venda)
        venda_item_formset = VendaItemFormSet(instance=venda)
        payment_method_formset = PaymentMethodVendaFormSet(instance=venda)

    context = {
        'venda_form': venda_form,
        'venda_item_formset': venda_item_formset,
        'payment_method_formset': payment_method_formset,
        'venda': venda,
    }

    return render(request, 'sale/venda_form.html', context)

@login_required# Deletar uma Venda
def venda_delete(request, pk):
    # Obtém a venda com base no id (pk)
    venda = get_object_or_404(Venda, pk=pk)
    # Recupera os itens de venda relacionados
    venda_items = VendaItem.objects.filter(venda=venda)
    # Restaura a quantidade dos produtos no estoque
    for item in venda_items:
        produto = item.product
        produto.current_quantity += item.quantidade  # Restaura a quantidade
        produto.save()
    # Exclui os itens de venda
    venda_items.delete()
    # Exclui a venda
    venda.delete()
    # Redireciona para a lista de vendas após a deleção
    return redirect('venda_list')

@login_required# Criar VendaItem para uma venda específica
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
    return render(request, 'sale/venda_item_form.html', {'form': form, 'venda': venda})


def client_search(request):
    """Busca clientes dinamicamente e retorna JSON."""
    query = request.GET.get('query', '') 
    resultados = Person.objects.filter(
        Q(id__icontains=query) | 
        Q(id_FisicPerson_fk__name__icontains=query) | 
        Q(id_ForeignPerson_fk__name_foreigner__icontains=query) | 
        Q(id_LegalPerson_fk__fantasyName__icontains=query)
    ).order_by('id')[:5]

    if not resultados:
        return JsonResponse({'clientes': [], 'message': 'Nenhum cliente encontrado.'})

    clients = [
        {
            'id': cliente.id,
            'name': (
                    cliente.id_FisicPerson_fk.name if cliente.id_FisicPerson_fk else 
                    (cliente.id_ForeignPerson_fk.name_foreigner if cliente.id_ForeignPerson_fk else 
                    (cliente.id_LegalPerson_fk.fantasyName if cliente.id_LegalPerson_fk else 'Nome não disponível')))
        }
        for cliente in resultados
    ]
    return JsonResponse({'clientes': clients})

def get_product_id(request):
    query = request.GET.get('query','')
    resultados = Product.objects.filter(
        Q(id=query) 
    )
    resultados_json = list(resultados.values("product_code","description"))
    print(resultados_json)
 
   
    return JsonResponse({'produto':resultados_json})
def product_search(request):
    query = request.GET.get('query','')
    resultados = Product.objects.filter(
        Q(product_code__icontains=query) |
        Q(description__icontains=query)
    ).order_by('id'[:5])

    products = [
        {
            'id':produto.id,
            'product_code':produto.product_code,
            'description':produto.description,
            'selling_price':produto.selling_price
        }
        for produto in resultados
        
    ]
    return JsonResponse({'produtos':products})

@login_required
def buscar_vendas(request):
    query = request.GET.get('query','').strip()
    page_num = request.GET.get('page',1)


    resultados = Venda.objects.filter(
        Q(id__istartswith=query) | 
        Q(pessoa__id_FisicPerson_fk__name__istartswith=query) |
        Q(pessoa__id_ForeignPerson_fk__name_foreigner__istartswith=query) |
        Q(pessoa__id_LegalPerson_fk__fantasyName__istartswith=query)
    ).order_by('id')

    sales = [
        {
            'id':venda.id,
            'pessoa':(
                venda.pessoa.id_FisicPerson_fk.name if venda.pessoa.id_FisicPerson_fk else
                (venda.pessoa.id_ForeignPerson_fk.name_foreigner if venda.pessoa.id_FisicPerson_fk else
                (venda.pessoa.LegalPerson_fk.fantasyName if venda.pessoa.LegalPerson_fk else 'Nome não disponível'))
            ),
            'data_da_venda':venda.data_da_venda,
            'situacao':venda.situacao.name_Situation,
            'is_active':venda.is_active
        } 
        for venda in resultados
    ]

    usuario_paginator = Paginator(sales,2)
    page = usuario_paginator.get_page(page_num)

    response_data = {
        'vendas':list(page.object_list),
        'pagination': {
            'has_previous': page.has_previous(),
            'previous_page': page.previous_page_number() if page.has_previous() else None,
            'has_next': page.has_next(),
            'next_page': page.next_page_number() if page.has_next() else None,
            'current_page': page.number,
            'total_pages': usuario_paginator.num_pages,
        },
        'message': f"{len(sales)} Vendas encontrados." if page.object_list else "Nenhum cliente encontrado."
    }

    return JsonResponse(response_data)