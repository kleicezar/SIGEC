from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *

### SALE

@login_required
def venda_list(request):
    vendas = Venda.objects.all()
    return render(request, 'sale/venda_list.html', {'vendas': vendas})

    # 
    # @login_requiredCriar uma nova Venda
    # def venda_create(request):
    #     if request.method == 'POST':
    #         form = VendaForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('venda_list')  # Redireciona para a lista de vendas
    #     else:
    #         form = VendaForm()
    #     return render(request, 'sale/venda_form.html', {'form': form})


    # 
    # @login_requiredCriar uma nova Venda com itens
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

    #     return render(request, 'sale/venda_form.html', {'venda_form': venda_form, 'venda_items': venda_items})

@login_required
def venda_create(request):
    VendaItemFormSet = inlineformset_factory(Venda, VendaItem, form=VendaItemForm, extra=1, can_delete=True)
    PaymentMethodVendaFormSet = inlineformset_factory(Venda, PaymentMethod_Venda, form=PaymentMethodVendaForm, extra=1, can_delete=True)
    # VendaItemFormSet = modelformset_factory(VendaItem, form=VendaItemForm, extra=1)
    # PaymentMethodVendaFormSet = modelformset_factory(PaymentMethod_Venda, form=PaymentMethodVendaForm, extra=1)
    
    if request.method == 'POST':
        venda_form = VendaForm(request.POST)
        venda_item_formset = VendaItemFormSet(request.POST)
        payment_method_formset = PaymentMethodVendaFormSet(request.POST)
        
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

                venda_item_formset.instance = venda
                venda_item_formset.save()
                
                # Salva os itens da venda
                for form in venda_item_formset:
                    if form.cleaned_data:
                        produto = form.cleaned_data['product']
                        quantidade = form.cleaned_data['quantidade']
                        preco_unitario = form.cleaned_data['preco_unitario']
                        
                        VendaItem.objects.create(
                            venda=venda,
                            product=produto,
                            quantidade=quantidade,
                            preco_unitario=preco_unitario
                        )
                        
                        produto.current_quantity -= quantidade
                        produto.save()

                # Salva as formas de pagamento associadas à venda
                for form in payment_method_formset:
                    if form.cleaned_data:
                        forma_pagamento = form.cleaned_data['forma_pagamento']
                        expiration_date = form.cleaned_data['expirationDate']
                        valor = form.cleaned_data['valor']
                        
                        PaymentMethod_Venda.objects.create(
                            venda=venda,
                            forma_pagamento=forma_pagamento,
                            expirationDate=expiration_date,
                            valor=valor
                        )
                
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
