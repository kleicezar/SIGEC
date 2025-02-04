
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from finance.models import PaymentMethod_Accounts
from finance.forms import PaymentMethodAccountsForm, AccountsForm


### PURCHASE

@login_required
def compras_list(request):
    compras = Compra.objects.all()
    return render(request, 'purchase/compras_list.html', {'compras': compras})

@login_required
def compras_create(request):
    CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)
    PaymentMethodCompraFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    
    PaymentMethodAccountsFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)

    if request.method == 'POST':
        compra_form = CompraForm(request.POST)
        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)
        compra_item_formset = CompraItemFormSet(request.POST)
        payment_method_formset = PaymentMethodCompraFormSet(request.POST)
        if compra_form.is_valid() and compra_item_formset.is_valid() and payment_method_formset.is_valid():
            
            compra = compra_form.save(commit=False)
            compra.save()  
            
            compra_item_formset.instance = compra
            compra_item_formset.save()

            # Atualizar estoque
            for form in compra_item_formset:
                if form.cleaned_data:
                    produto = form.cleaned_data['produto']
                    quantidade = form.cleaned_data['quantidade']
                    produto.current_quantity += quantidade
                    produto.save()


            payment_method_formset.instance = compra
            total_payment = 0
            valid_payments = []
            payments_to_delete = []
            print('OLÁ')
            print(payment_method_formset)
            print('Olá 2')
            for form in payment_method_formset:
                if form.cleaned_data:
                    form.acc = True
                    if form.cleaned_data.get("DELETE", False):
                        payments_to_delete.append(form.instance)
                    else:
                        valor = form.cleaned_data['value']
                        total_payment += valor
                        valid_payments.append(form)

            # Verificar se os pagamentos somam corretamente antes de salvar
            if total_payment == compra.total_value:
                for form in valid_payments:
                    form.instance.compra = compra  # Garante que a compra está associada
                    form.save()

                # Remover pagamentos marcados para exclusão
                for payment in payments_to_delete:
                    payment.delete()

                return redirect('compras_list')
            else:
                messages.warning(request, "Ação cancelada! O valor total dos pagamentos não corresponde ao total da compra.")
        if not compra_form.is_valid():
            print("Erro no CompraForm",compra_form.errors)
        if not compra_item_formset.is_valid():
            print("Erro no compraItem",compra_item_formset.errors)
        if not payment_method_formset.is_valid():
            print("Erro no paymentmethod",payment_method_formset.errors)
        compra_form = CompraForm()
        compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
        payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Accounts.objects.none())

    else:
        form_Accounts = AccountsForm()
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        compra_form = CompraForm()
        compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
        payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Accounts.objects.none())

    context = {
        'form_Accounts': form_Accounts,
        'form_payment_account': PaymentMethod_Accounts_FormSet,
        'compra_form': compra_form,
        'compra_item_formset': compra_item_formset,
        'payment_method_formset': payment_method_formset
    }
    return render(request, 'purchase/compras_form.html', context)

@login_required
def compras_update(request, pk):
    # Recupera a instância da Compra existente
    compra = get_object_or_404(Compra, pk=pk)

    # Configuração do formset para itens de compra e métodos de pagamento
    CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=0, can_delete=True)
    PaymentMethodCompraFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=0, can_delete=True)

    if request.method == 'POST':
        # Recupera os dados do formulário de compra e formsets de itens e métodos de pagamento
        compra_form = CompraForm(request.POST, instance=compra)
        compra_item_formset = CompraItemFormSet(request.POST, instance=compra)
        payment_method_formset = PaymentMethodCompraFormSet(request.POST, instance=compra)
        print(request.POST)
        if compra_form.is_valid() and compra_item_formset.is_valid() and payment_method_formset.is_valid():
            # Salva a compra (atualiza os dados da compra)
            print(compra_item_formset)
            compra_form.save(commit=False)
            compra_item_instances = compra_item_formset.save(commit=False)
            print(compra_item_instances)
            compra_item_formset.save_m2m()
            # Atualiza os itens de compra
            # compra_item_formset.save()
            for form in compra_item_formset:
                print('observando')
                if form.cleaned_data:
                    produto = form.cleaned_data['produto']
                    quantidade = form.cleaned_data['quantidade']
                    preco_unitario = form.cleaned_data['preco_unitario']
                    discount = form.cleaned_data['discount']
                    price_total = form.cleaned_data['price_total']
                    delete = form.cleaned_data["DELETE"]

                    item_id = form.instance.id
                    try:
                        compra_item_quantidade = CompraItem.objects.get(id=item_id).quantidade  
                        if not delete:
                            # SALVA A QUANTIDADE ATUAL DE PRODUTOS - COMPRAITENS QUE JA EXISTIAM
                            produto.current_quantity =  produto.current_quantity + form.cleaned_data['quantidade']- compra_item_quantidade 

                            # print(produto.current_quantity - compra_item_quantidade + form.cleaned_data['quantidade'] )
                            produto.save()
                        else:
                            if not delete:  
                                print('entrei')
                                CompraItem.objects.create(
                                    compra = compra,
                                    product = produto,
                                    quantidade = quantidade,
                                    preco_unitario = preco_unitario,
                                    discount = discount,
                                    price_total = price_total
                                )
                            # RETORNA A QUANTIDADE ATUAL DE PRODUTOS - COMPRAITENS MARCADOS PARA SER EXCLUIDOS
                            produto.current_quantity = produto.current_quantity - compra_item_quantidade
                            produto.save()
                    except:
                        # SALVA A QUANTIDADE ATUAL DE PRODUTOS - NOVO COMPRA ITENS
                        produto.current_quantity += quantidade
                        produto.save()  

            itens_para_deletar = []
            for form in compra_item_formset.deleted_forms:
                if form.instance.pk is not None:
                    itens_para_deletar.append(form.instance)
            print()
            print(compra_item_instances)
            for instance in compra_item_instances:
                print('instac')
                print(instance)
                instance.save()

            for item in itens_para_deletar:
                item.delete()
            


            payments_intances = compra_item_formset.save(commit=False)
            # payment_method_formset.save_m2m()
          
            pagamentos_para_deletar = []
            for form in payment_method_formset.deleted_forms:
                if form.instance.pk is not None:
                    pagamentos_para_deletar.append(form.instance)


            for instance in payments_intances:
                instance.save()
            
            for pagamento in pagamentos_para_deletar:
                pagamento.delete()
            # venda_item_formset.save()
            payment_method_formset.save()

            messages.success(request,"Compra atualizada com sucesso!")
            return redirect('compras_list')
            # Atualiza o estoque, adicionando as quantidades compradas
            # for form in compra_item_formset:
               
            # Salva as formas de pagamento associadas à compra
            # payment_method_formset.save()

            # Redireciona para a lista de compras após a atualização
        if not compra_form.is_valid():
            print('Erro no CompraForms', compra_form.errors)
        if not compra_item_formset.is_valid():
            print("Erro no CompraItem",compra_item_formset.errors)
        if not payment_method_formset.is_valid():
            print("Erro na FormPagamento",payment_method_formset.errors)

    else:
        # Se for um GET, inicializa o formulário com os dados da compra existente
        form_Accounts = AccountsForm()
        compra_form = CompraForm(instance=compra)
        payment_method_formset = PaymentMethodCompraFormSet(queryset=compra.paymentmethod_accounts_set.all(), instance=compra)
        compra_item_formset = CompraItemFormSet(queryset=compra.compraitem_set.all(), instance=compra)
      
        payment_methods_qs = compra.paymentmethod_accounts_set.all()
        # compra = Compra.objects.last()
        # Ou compra.metodos_pagamento.all()
        pagamentos = PaymentMethod_Accounts.objects.filter(compra=compra)

        for form in payment_method_formset:
            # obj = form.instance
            # print(f"ID: {obj.id}, Valor: {obj.value}, Método: {obj.payment_method}, Conta: {obj.account_number}")
            print(form) 
         #Testar no 4


        # payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Accounts)

    context = {
        'form_Accounts':form_Accounts,
        'compra_form': compra_form,
        'compra_item_formset': compra_item_formset,
        'form_payment_account': payment_method_formset,
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

def get_product_id(request):
    query = request.GET.get('query','')
    resultados = Product.objects.filter(
        Q(id=query) 
    )
    resultados_json = list(resultados.values("product_code","description"))
    print(resultados_json)
 
   
    return JsonResponse({'produto':resultados_json})