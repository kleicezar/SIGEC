
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout

from Sale.models import Venda, VendaItem

from Service.models import VendaItem as VendaItemWS
from .forms import *
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from finance.models import PaymentMethod_Accounts
from finance.forms import PaymentMethodAccountsForm, AccountsForm


### PURCHASE

@login_required
def productsWithStatus_list(request):
    vendasItens = VendaItem.objects.all()
    workOrders = VendaItemWS.objects.all()
    status_options = ["Pendente", "Entregue"]

    all_products_with_status = [
        {'idVenda': vendaItem.venda.id,'idProduto':vendaItem.product.id,'idVendaItem':vendaItem.id,'descricao': vendaItem.product.description, 'quantidade': vendaItem.quantidade, 'status': vendaItem.status} for vendaItem in vendasItens
    ] + [
        {'idVenda': workOrder.venda.id, 'idProduto':workOrder.product.id,'idVendaItem':workOrder.id,'descricao': workOrder.product.description, 'quantidade': workOrder.quantidade,'status':workOrder.status} for workOrder in workOrders
    ]

    return render(request, 'purchase/manageDeliveries_list.html', {
        'all_products_with_status': all_products_with_status,
        "status_options": status_options

    })

@login_required
def update_product_quantity(request,pk):
    if request.method == "POST":
        id_venda = request.POST.get("id_venda")
        print('venda id')
        print(id_venda)
        vendaitem = get_object_or_404(VendaItem,pk=id_venda)
        vendaitem.status = "Entregue"
        vendaitem.save()
        product = get_object_or_404(Product,pk=pk)
        product.current_quantity-= vendaitem.quantidade

        if product.current_quantity >= vendaitem.quantidade:
            product.save()
        else:
            print("QUANTIDADE DE PRODUTOS MENOR QUE A SOLICITADA")
        
    return redirect('manageProductDelivery')
@login_required
def compras_list(request):
    compras = Compra.objects.all()
    return render(request, 'purchase/compras_list.html', {'compras': compras})

@login_required
def compras_create(request):
    CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)
    # PaymentMethodCompraFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    
    PaymentMethodAccountsFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    if request.method == 'POST':
        compra_form = CompraForm(request.POST)
        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)
        compra_item_formset = CompraItemFormSet(request.POST)
        # payment_method_formset = PaymentMethodCompraFormSet(request.POST)
        if compra_form.is_valid() and compra_item_formset.is_valid() and PaymentMethod_Accounts_FormSet.is_valid():
            
            compra = compra_form.save(commit=False)
            # compra.save()  
            
            compra_item_formset.instance = compra
            compra_item_formset.save(commit=False) 

            print(f"Total de formulários processados: {compra_item_formset.total_form_count()}")
            # compra_item_formset.save()

            # Atualizar estoque
            for form in compra_item_formset:
                if form.cleaned_data:
                    produto = form.cleaned_data['produto']
                    quantidade = form.cleaned_data['quantidade']
                    # values = form.cleaned_data['value']
                    produto.current_quantity += quantidade
                    produto.save()


            PaymentMethod_Accounts_FormSet.instance = compra
            total_payment = 0
            valid_payments = []
            payments_to_delete = []
            # print(payment_method_formset)
            for form in PaymentMethod_Accounts_FormSet:
                if form.cleaned_data:
                    form.acc = True
                    valor = form.cleaned_data['value']
                    total_payment+=valor

                    # print(form.cleaned_data.get("acc"))
                    # if form.cleaned_data.get("DELETE", False):
                    #     payments_to_delete.append(form.instance)
                    # else:
                    #     valor = form.cleaned_data['value']
                    #     total_payment += valor
                    #     valid_payments.append(form)

            # Verificar se os pagamentos somam corretamente antes de salvar
            if total_payment == compra.total_value:
                compra_form.save()
                compra_item_formset.save()
                PaymentMethod_Accounts_FormSet.save()
                # for form in valid_payments:
                #     form.instance.acc = True
                #     form.instance.compra = compra  # Garante que a compra está associada
                #     form.save()

                # # Remover pagamentos marcados para exclusão
                # for payment in payments_to_delete:
                #     payment.delete()

                return redirect('compras_list')
            else:
                messages.warning(request, "Ação cancelada! O valor total dos pagamentos não corresponde ao total da compra.")
        if not compra_form.is_valid():
            print("Erro no CompraForm",compra_form.errors)

        if not compra_item_formset.is_valid():
            print("Erro no CompraItem",compra_item_formset.errors)

        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no PaymentMethod",PaymentMethod_Accounts_FormSet.errors)

        compra_form = CompraForm()
        compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
        # payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Accounts.objects.none())

    else:
        form_Accounts = AccountsForm()
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        compra_form = CompraForm()
        compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
        # payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Accounts.objects.none())

    context = {
        'form_Accounts': form_Accounts,
        'form_payment_account': PaymentMethod_Accounts_FormSet,
        'compra_form': compra_form,
        'compra_item_formset': compra_item_formset,
        # 'payment_method_formset': payment_method_formset
    }
    return render(request, 'purchase/compras_form.html', context)

@login_required
def compras_update(request, pk):
    # Recupera a instância da Compra existente
    compra = get_object_or_404(Compra, pk=pk)

    # Configuração do formset para itens de compra e métodos de pagamento
    CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=0, can_delete=True)
    # PaymentMethodCompraFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=0, can_delete=True)

    PaymentMethodAccountsFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    Older_PaymentMethod_Accounts_Formset = inlineformset_factory(Compra,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=0,can_delete=True)
    # print(request.POST)
    if request.method == 'POST':
        # Recupera os dados do formulário de compra e formsets de itens e métodos de pagamento
        compra_form = CompraForm(request.POST, instance=compra)
        compra_item_formset = CompraItemFormSet(request.POST, instance=compra)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST,instance=compra)
        Older_PaymentMethod_Accounts_FormSet = Older_PaymentMethod_Accounts_Formset(request.POST,instance=compra,prefix="older_paymentmethod_accounts_set")

        compra_item = CompraItem.objects.filter(compra=compra)
        ids_existentes_compra_itens = set(compra_item.values_list('id',flat=True))

        ids_enviados_compra_itens = set(
            int(value) for key,value in request.POST.items()
            if key.startswith("compraitem_set-") and key.endswith("id") and value.isdigit()
        )
        
        ids_para_excluir_compra_itens = ids_existentes_compra_itens - ids_enviados_compra_itens

        compraitems_excluir = CompraItem.objects.filter(id__in=ids_para_excluir_compra_itens)
        for compra in compraitems_excluir:
            produto_id = compra.produto.id
            produto = get_object_or_404(Product,pk = produto_id)

            produto.current_quantity = produto.current_quantity + compra.quantidade
            # produto_quanti = produto_quanti + compra.quantidade
      
            produto.save()
        compraitems_excluir.delete()
        if compra_form.is_valid() and compra_item_formset.is_valid() and PaymentMethod_Accounts_FormSet.is_valid():
            # Salva a compra (atualiza os dados da compra)
            compra_form.save(commit=False)
            compra_item_instances = compra_item_formset.save(commit=False)

            compra_item_formset.save_m2m()
            # Atualiza os itens de compra

            for form in compra_item_formset:
                
                if form.cleaned_data:
                    produto = form.cleaned_data['produto']
                    quantidade = form.cleaned_data['quantidade']
                    item_id = form.instance.id
                    try:
                        compra_item_quantidade = CompraItem.objects.get(id=item_id).quantidade  
                        # SALVA A QUANTIDADE ATUAL DE PRODUTOS - COMPRAITENS QUE JA EXISTIAM
                        produto.current_quantity = produto.current_quantity + form.cleaned_data['quantidade'] - compra_item_quantidade 
                        produto.save()
                    
                        # RETORNA A QUANTIDADE ATUAL DE PRODUTOS - COMPRAITENS MARCADOS PARA SER EXCLUIDOS
                        produto.current_quantity = produto.current_quantity - compra_item_quantidade
                        produto.save()
                    except:
                        # SALVA A QUANTIDADE ATUAL DE PRODUTOS - NOVO COMPRA ITENS
                        produto.current_quantity += quantidade
                        produto.save()  

            for instance in compra_item_instances:
                instance.save()

            itens_para_deletar = []
            for form in compra_item_formset.deleted_forms:
                if form.instance.pk is not None:
                    itens_para_deletar.append(form.instance)

            for item in itens_para_deletar:
                item.delete()
        
            total_payment = 0
            for form in PaymentMethod_Accounts_FormSet:
                if form.cleaned_data:
                    if not form.cleaned_data.get("DELETE"):
                        valor = form.cleaned_data['value']
                        total_payment += valor
                    
            if total_payment == compra_form.cleaned_data['total_value']:
                compra_form.save()

                for instance in compra_item_instances:
                    instance.save()

                for item in itens_para_deletar:
                    item.delete()
                
                if len(PaymentMethod_Accounts_FormSet) > 0:

                    if len(PaymentMethod_Accounts_FormSet) >= len(Older_PaymentMethod_Accounts_FormSet):

                        for old_form, new_form in zip(Older_PaymentMethod_Accounts_FormSet, PaymentMethod_Accounts_FormSet):
                            old_instance = old_form.instance
                            new_instance = new_form.instance

                            old_instance.forma_pagamento = new_instance.forma_pagamento
                            old_instance.expirationDate = new_instance.expirationDate
                            old_instance.days = new_instance.days
                            old_instance.value = new_instance.value

                            old_instance.save()

                            new_form.cleaned_data["DELETE"] = True
                        
                        Older_PaymentMethod_Accounts_FormSet.save()
                        PaymentMethod_Accounts_FormSet.save() 
            

                    else:
                    # FALTA VERIFICAR ESSA
                    # atualizar os formulários existentes
                        for old_form, new_form in zip(Older_PaymentMethod_Accounts_FormSet, PaymentMethod_Accounts_FormSet):
                            old_instance = old_form.instance
                            new_instance = new_form.instance

                            old_instance.forma_pagamento = new_instance.forma_pagamento
                            old_instance.expirationDate = new_instance.expirationDate
                            old_instance.days = new_instance.days
                            old_instance.value = new_instance.value

                            old_instance.save()

                        # remover os formulários extras de Older_PaymentMethod_Accounts_FormSet
                        for extra_form in Older_PaymentMethod_Accounts_FormSet[len(PaymentMethod_Accounts_FormSet):]:
                            extra_form.instance.delete()

                        Older_PaymentMethod_Accounts_FormSet.save()                            

            if total_payment != compra_form.cleaned_data["total_value"]:
                messages.warning(request, "Ação cancelada! O valor total dos pagamentos não corresponde ao total da compra.")

            messages.success(request,"Compra atualizada com sucesso!")
            return redirect('compras_list')
            # Atualiza o estoque, adicionando as quantidades compradas
        if not compra_form.is_valid():
            print('Erro no CompraForms', compra_form.errors)

        if not compra_item_formset.is_valid():
            print("Erro no CompraItem",compra_item_formset.errors)
            
        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro na FormPagamento",PaymentMethod_Accounts_FormSet.errors)
        return redirect("compras_list")
    else:
        # Se for um GET, inicializa o formulário com os dados da compra existente
        form_Accounts = AccountsForm(instance=compra)
        Older_PaymentMethod_Accounts_Formset = Older_PaymentMethod_Accounts_Formset(queryset=compra.paymentmethod_accounts_set.all(),instance=compra,prefix="older_paymentmethod_accounts_set")
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        compra_form = CompraForm(instance=compra)
        # payment_method_formset = PaymentMethodCompraFormSet(queryset=compra.paymentmethod_accounts_set.all(), instance=compra)
        compra_item_formset = CompraItemFormSet(queryset=compra.compraitem_set.all(), instance=compra)
        count_payment = 0
       
        for i,form in enumerate(Older_PaymentMethod_Accounts_Formset):
            if i == 0:
                data_obj = form.initial["expirationDate"]  
                data_modificada = data_obj - timedelta(days=int(form.initial["days"])) 
                data_modificada = datetime.strptime(str(data_modificada), "%Y-%m-%d").strftime("%d/%m/%Y") 

            count_payment+=1
        form_Accounts.initial["date_init"] = data_modificada
        form_Accounts.initial["totalValue"] = compra_form.initial['total_value']
        form_Accounts.initial["numberOfInstallments"] = count_payment

        # payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Accounts)

        context = {
            'form_Accounts':form_Accounts,
            'form_payment_account':PaymentMethod_Accounts_FormSet,
            'compra_form': compra_form,
            'compra_item_formset': compra_item_formset,
            'older_form_payment_account':Older_PaymentMethod_Accounts_Formset
            # 'form_payment_account': payment_method_formset,
        }
        return render(request, 'purchase/compras_formUpdate.html', context)

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
        produto.current_quantity -= item.quantidade
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
@permission_required('purchase.view_product', raise_exception=True)
def product(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'purchase/product_list.html', {'products': products})

@login_required
@permission_required('purchase.add_product', raise_exception=True)
def productForm(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Product')
        else:
            print('Erro no formulário de produto:',form.errors)
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
    product.is_active = False
    product.save()
    return redirect('Product')

@login_required
def buscar_produtos(request):
    query = request.GET.get('query','').strip()
    page_num = request.GET.get('page',1)

    resultados = Product.objects.filter(
        (
            Q(id__istartswith=query) |
            Q(description__istartswith=query) |
            Q(product_code__istartswith=query)
        )
        & Q(is_active = True)
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

def get_product_id(request):
    query = request.GET.get('query','')
    resultados = Product.objects.filter(
        Q(id=query) 
    )
    resultados_json = list(resultados.values("product_code","description"))
    print(resultados_json)
 
   
    return JsonResponse({'produto':resultados_json})