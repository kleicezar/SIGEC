
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from operator import attrgetter
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.db.models.functions import Coalesce
from django.db.models import F, Value
from registry.models import Credit
from sale.forms import ReturnVendaItemForm, VendaItemForm, VendaItemFormExpedition
from sale.models import Venda, VendaItem
# from service.models import VendaItem as VendaItemWS
from .forms import *
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from finance.models import  PaymentMethod_Accounts
from finance.forms import  PaymentMethodAccountsForm, AccountsForm
from django.db import transaction

### PURCHASE

@login_required
def productsWithStatus_list(request):

    vendasItens = VendaItem.objects.filter(
        Q(status = 'Pendente')
    )
    # workOrders = VendaItemWS.objects.filter(
    #     Q(status = 'Pendente')
    # )
    status_options = ["Pendente", "Entregue"]

    all_products_with_status = [
        {
            'idVenda': vendaItem.venda.id if vendaItem.venda else None,
            'idVendaServico':vendaItem.servico.id if vendaItem.servico else None,
            'idProduto':vendaItem.product.id,
            'idVendaItem':vendaItem.id,
            'descricao': vendaItem.product.description, 
            'quantidade': vendaItem.quantidade, 
            'status': vendaItem.status
        } for vendaItem in vendasItens
    ]
    # messages.warning(request,'TESTE',extra_tags='delivery_page')
    return render(request, 'purchase/manageDeliveries_list.html', {
        'all_products_with_status': all_products_with_status,
        "status_options": status_options,
        'type':'Pendente'

    })

@login_required
@transaction.atomic
def update_product_quantity(request,pk):
    if request.method == "POST":
        id_venda = request.POST.get("id_venda")
        vendaitem = get_object_or_404(VendaItem,pk=id_venda)
        vendaitem.status = "Entregue"
        vendaitem.save()
        product = get_object_or_404(Product,pk=pk)
        product.current_quantity-= vendaitem.quantidade

        if product.current_quantity >= vendaitem.quantidade:
            product.save()
        else:
            messages.warning(request,"Estoque do produto acabou.",extra_tags='delivery_page')
            print("QUANTIDADE DE PRODUTOS MENOR QUE A SOLICITADA")
        
    return redirect('manageProductDelivery')

@login_required
def compras_list(request):
    sort = request.GET.get('sort')
    direction = request.GET.get('dir','asc')
   
    if not sort:
        compras = Compra.objects.all().order_by()
    else:
        if direction == 'desc':
            ordering = f'-{sort}'
        else:
            ordering = sort

        if ordering == 'fornecedor':
            fisicName  = f'fornecedor__id_FisicPerson_fk__name'
            legalPerson = f'fornecedor__id_LegalPerson_fk__fantasyName'
            foreignPerson = f'fornecedor__id_ForeignPerson_fk__name_foreigner'
            compras = Compra.objects.annotate(
                ordened_name = Coalesce(
                    F(fisicName),
                    F(legalPerson),
                    F(foreignPerson),
                    Value('')
                )
            ).order_by('ordened_name')
        elif ordering == '-fornecedor':
            fisicName  = f'fornecedor__id_FisicPerson_fk__name'
            legalPerson = f'fornecedor__id_LegalPerson_fk__fantasyName'
            foreignPerson = f'fornecedor__id_ForeignPerson_fk__name_foreigner'
            compras = Compra.objects.annotate(
                ordened_name = Coalesce(
                    F(fisicName),
                    F(legalPerson),
                    F(foreignPerson),
                    Value('')
                )
            ).order_by('-ordened_name')
        else:
            compras = Compra.objects.all().order_by(ordering)
    colunas = [
    ('id', 'ID'),
    ('fornecedor', 'Pessoa'),
    ('situacao', 'Situação')
    ]
    # compras = Compra.objects.all()
    context = {
        'colunas':colunas,
        'compras':compras,
        'current_sort':sort,
        'current_dir':direction
    }
   
    return render(request, 'purchase/compras_list.html', context)

@login_required
@transaction.atomic
def compras_create(request):

    def calculateValuePayments(paymentForm):
        total_by_purpose = {} 
        for form in paymentForm:
            if form.cleaned_data:
                purpose = form.cleaned_data.get('paymentPurpose')
                value = form.cleaned_data.get('value', 0)
                if purpose:  # Só processa se tiver propósito
                    total_by_purpose[purpose] = total_by_purpose.get(purpose, 0) + value

                form.instance.acc = True  # Atualiza o campo acc

        return total_by_purpose
    
    def savePayments(paymentForm):
        for form in paymentForm:
            conta = form.save(commit=False)  # cria o objeto sem salvar ainda
            conta.compra = compra            # agora sim associa corretamente
            conta.acc = True
            conta.save() 

    CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)

    if request.method == 'POST':
        compra_form = CompraForm(request.POST)

        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)


        frete_form = FreteForm(request.POST)
        rmn_form = RomaneioForm(request.POST)
        imposto_form = TaxForm(request.POST)

        compra_form.new_payment_formset = PaymentMethod_Accounts_FormSet
        compra_form.new_form_flag = request.POST.get('new_form', '').lower() in ['true', '1', 'yes', 'on']

        compra_item_formset = CompraItemFormSet(request.POST)
        
        if (
            PaymentMethod_Accounts_FormSet.is_valid() and
            compra_form.is_valid() and 
            compra_item_formset.is_valid() and 
            frete_form.is_valid() and
            rmn_form.is_valid() and
            imposto_form.is_valid() 
           
            ):
            
            compra = compra_form.save(commit=False)
            compra_item_formset.instance = compra
            compra_item_formset.save(commit=False) 


            print(f"Total de formulários processados: {compra_item_formset.total_form_count()}")
            # Atualizar estoque
            for form in compra_item_formset:
                if form.cleaned_data:
                    produto = form.cleaned_data['produto']
                    quantidade = form.cleaned_data['quantidade']
    
                    produto.current_quantity += quantidade
                    produto.save()

            
            PaymentMethod_Accounts_FormSet.instance = compra
            total_by_purpose = calculateValuePayments(PaymentMethod_Accounts_FormSet)

            valueTotalProduct = total_by_purpose['Produto']

            if valueTotalProduct == compra.total_value:

                compra.save()
                compra_item_formset.save()
                savePayments(PaymentMethod_Accounts_FormSet)
                
                if compra_form.cleaned_data['taxExists']:
                    valueTotalTax = total_by_purpose['Imposto']
                    if valueTotalTax == imposto_form.cleaned_data['valueTax']:
                        imposto = imposto_form.save(commit=False)
                        imposto.compra = compra
                        imposto.save()

                if compra_form.cleaned_data['rmnExists']:
                    valueTotalRMN = total_by_purpose['Romaneio']
                    if valueTotalRMN == rmn_form.cleaned_data['valuePickingList']:
                        rmn = rmn_form.save(commit=False)
                        rmn.compra = compra
                        rmn.save()

                if compra_form.cleaned_data['freightExists']:
                    valueTotalFreight = total_by_purpose['Frete']
                    if valueTotalFreight == frete_form.cleaned_data['valueFreight']:
                        frete= frete_form.save(commit=False)
                        frete.compra = compra
                        frete.save()
               
                return redirect('compras_list')
                    
        if not compra_form.is_valid():
            print("Erro no CompraForm",compra_form.errors)

        if not compra_item_formset.is_valid():
            print("Erro no CompraItem",compra_item_formset.errors)

        if not frete_form.is_valid():
            print('Erro no Frete',frete_form.errors)

        if not rmn_form.is_valid():
            print('Erro no Romaneio',rmn_form.errors)

        if not imposto_form.is_valid():
            print('Erro no Imposto',imposto_form.errors)

        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no PaymentMethod",PaymentMethod_Accounts_FormSet.errors)

        return redirect('compras_create')

    else:
        form_Accounts = AccountsForm()
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        frete = FreteForm()
        romaneio = RomaneioForm()
        imposto = TaxForm()
        compra_form = CompraForm()
        compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
       

    context = {
        'form_Accounts': form_Accounts,
        'form_payment_account': PaymentMethod_Accounts_FormSet,
        'compra_form': compra_form,
        'compra_item_formset': compra_item_formset,
        'frete_form':frete,
        'rmn_form':romaneio,
        'tax_form':imposto
    }
    return render(request, 'purchase/compras_form.html', context)

@login_required
@transaction.atomic 
def compras_update(request, pk):

    def calculate_value_payments_update(paymentForm):
        total_by_purpose = {} 
        for form in paymentForm:
            if form.cleaned_data:
                purpose = form.cleaned_data.get('paymentPurpose')
                value = form.cleaned_data.get('value', 0)
                if purpose:  # Só processa se tiver propósito
                    total_by_purpose[purpose] = total_by_purpose.get(purpose, 0) + value

                form.instance.acc = True  # Atualiza o campo acc

        return total_by_purpose
    
    def rearrange_payments(onlyOldPayments, paymentForm, olderPaymentForm):
        if not onlyOldPayments:
            if len(paymentForm) >= len(olderPaymentForm):
                for old_form, new_form in zip(olderPaymentForm, paymentForm):
                    old_instance = old_form.instance
                    new_instance = new_form.instance

                    old_instance.forma_pagamento = new_instance.forma_pagamento
                    old_instance.paymentPurpose = new_instance.paymentPurpose
                    old_instance.expirationDate = new_instance.expirationDate
                    old_instance.days = new_instance.days
                    old_instance.value = new_instance.value
                    old_instance.acc = True

                    old_instance.save()

                    new_form.cleaned_data["DELETE"] = True

                olderPaymentForm.save()

                for form in paymentForm:
                    form_instance = form.instance
                    form_instance.acc = True
                    # form_instance.save()
                paymentForm.save()

            else:
                # atualizar os formulários existentes
                for old_form, new_form in zip(olderPaymentForm, paymentForm):
                    old_instance = old_form.instance
                    new_instance = new_form.instance

                    old_instance.forma_pagamento = new_instance.forma_pagamento
                    old_instance.paymentPurpose = new_instance.paymentPurpose
                    old_instance.expirationDate = new_instance.expirationDate
                    old_instance.days = new_instance.days
                    old_instance.value = new_instance.value
                    old_instance.acc = True

                    old_instance.save()

                # remove os formulários extras de Older_PaymentMethod_Accounts_FormSet
                for extra_form in olderPaymentForm[len(paymentForm):]:
                    extra_form.instance.delete()

                olderPaymentForm.save()
        else:
            # Atualiza acc para True mesmo se só estiver usando os formulários antigos
            for old_form in olderPaymentForm:
                old_instance = old_form.instance
                old_instance.acc = True
                # old_instance.save()
                
            olderPaymentForm.save()


    def populate_account_form(olderForm,form_Payment_Accounts):
        count_payment = 0
        value_total_payment = 0
        for i,form in enumerate(olderForm):
            if i == 0:
                data_obj = form.initial["expirationDate"]  
                data_modificada = data_obj - timedelta(days=int(form.initial["days"])) 
                data_modificada = datetime.strptime(str(data_modificada), "%Y-%m-%d").strftime("%d/%m/%Y") 
                
            value_total_payment+= form.initial["value"]
                
            count_payment+=1
        form_Payment_Accounts.initial["date_init"] = data_modificada
        form_Payment_Accounts.initial["totalValue"] = compra_form.initial['total_value']
        form_Payment_Accounts.initial["numberOfInstallments"] = count_payment

        return form_Payment_Accounts
    # Recupera a instância da Compra existente
    compra = get_object_or_404(Compra, pk=pk)

    CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=0, can_delete=True)

    PaymentMethodAccountsFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    Older_PaymentMethod_Accounts_Formset = inlineformset_factory(Compra,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=0,can_delete=True)

    if request.method == 'POST':
        # Recupera os dados do formulário de compra e formsets de itens e métodos de pagamento
        compra_form = CompraForm(request.POST, instance=compra)
        compra_item_formset = CompraItemFormSet(request.POST, instance=compra)

        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST,instance=compra)
        Older_PaymentMethod_Accounts_FormSet = Older_PaymentMethod_Accounts_Formset(request.POST,instance=compra,prefix="older_paymentmethod_accounts_set")

        frete_instance = compra.frete_set.first()
        frete_form = FreteForm(request.POST,instance=compra)

        rmn_instance = compra.pickinglist_set.first()
        rmn_form = RomaneioForm(request.POST,instance=rmn_instance)

        tax_instance = compra.tax_set.first()
        tax_form = TaxForm(request.POST,instance=tax_instance)

        compra_item = CompraItem.objects.filter(compra=compra)

        # -----------------------------------------------------
        # PARTE RESPONSÁVEL POR ELIMINAR ITENS QUE EXISTE NO BANCO E QUE NAO FORAM ENVIADOs VIA REQUISIÇÃO POST
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
            produto.save()

        compraitems_excluir.delete()
        

        # -----------------------------------------------------

        if (
            PaymentMethod_Accounts_FormSet.is_valid() and 
            Older_PaymentMethod_Accounts_FormSet.is_valid() and
            compra_form.is_valid() and 
            compra_item_formset.is_valid() and 
            frete_form.is_valid() and
            rmn_form.is_valid() and 
            tax_form.is_valid() 
            
            ):
            # Salva a compra (atualiza os dados da compra)
            compra_item_instances = compra_item_formset.save(commit=False)
            
            value_new_form = request.POST.get('new_form','').lower()
            has_new_form = value_new_form in ['true', '1', 'on', 'yes']

            compra_form.new_payment_formset = PaymentMethod_Accounts_FormSet
            compra_form.old_payment_formset = Older_PaymentMethod_Accounts_FormSet
            compra_form.new_form_flag = request.POST.get('new_form', '').lower() in ['true', '1', 'yes', 'on']

            if has_new_form:

                onlyOldPayments = False
                total_by_purpose = calculate_value_payments_update(PaymentMethod_Accounts_FormSet)
            else:

                onlyOldPayments = True
                total_by_purpose = calculate_value_payments_update(Older_PaymentMethod_Accounts_FormSet)

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
            
            valueTotalProduct = total_by_purpose['Produto']
            if valueTotalProduct == compra.total_value:
                # Salva a compra atual
                compra.save()
                compra_item_formset.save()
                rearrange_payments(
                    onlyOldPayments,
                    PaymentMethod_Accounts_FormSet,
                    Older_PaymentMethod_Accounts_FormSet
                )

                # IMPOSTO
                if compra_form.cleaned_data.get('taxExists'):
                    valueTotalTax = total_by_purpose.get('Imposto', 0)
                    if valueTotalTax == tax_form.cleaned_data.get('valueTax'):
                        imposto = tax_form.save(commit=False)
                        imposto.compra = compra
                        imposto.save()
                elif tax_form.instance.pk:
                    tax_form.instance.delete()

                # ROMANEIO
                if compra_form.cleaned_data.get('rmnExists'):
                    valueTotalRMN = total_by_purpose.get('Romaneio', 0)
                    if valueTotalRMN == rmn_form.cleaned_data.get('valuePickingList'):
                        rmn = rmn_form.save(commit=False)
                        rmn.compra = compra
                        rmn.save()
                elif rmn_form.instance.pk:
                    valueTotalRMN = total_by_purpose.get('Romaneio', 0)
                    rmn_form.instance.delete()

                # FRETE
                if compra_form.cleaned_data.get('freightExists'):
                    valueTotalFreight = total_by_purpose.get('Frete', 0)
                    if valueTotalFreight == frete_form.cleaned_data.get('valueFreight'):
                        frete = frete_form.save(commit=False)
                        frete.compra = compra
                        frete.save()
                elif frete_form.instance.pk:
                    frete_form.instance.delete()

                return redirect('compras_list')        
            
        if not compra_form.is_valid():
            print('Erro no CompraForms', compra_form.errors)

        if not compra_item_formset.is_valid():
            print("Erro no CompraItem",compra_item_formset.errors)
            
        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro na PaymentMethod_Accounts_FormSet",PaymentMethod_Accounts_FormSet.errors)
        
        if not Older_PaymentMethod_Accounts_FormSet.is_valid():
            print('Erro no Older_PaymentMethod_Accounts_FormSet',Older_PaymentMethod_Accounts_FormSet.errors)

        return redirect('compras_update',pk=pk)
        
    else:
        # Se for um GET, inicializa o formulário com os dados da compra existente
        form_Accounts = AccountsForm(instance=compra)
        Older_PaymentMethod_Accounts_Formset = Older_PaymentMethod_Accounts_Formset(queryset=compra.paymentmethod_accounts_set.all(),instance=compra,prefix="older_paymentmethod_accounts_set")
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())

        frete_instance = compra.frete_set.first()  # ou .get() se for só um
        frete_form = FreteForm(instance=frete_instance)

        rmn_instance = compra.pickinglist_set.first()
        rmn_form = RomaneioForm(instance=rmn_instance)

        tax_instance = compra.tax_set.first()
        tax_form = TaxForm(instance=tax_instance)

        compra_form = CompraForm(instance=compra)
        compra_item_formset = CompraItemFormSet(queryset=compra.compraitem_set.all(), instance=compra)
        
        form_Accounts = populate_account_form(Older_PaymentMethod_Accounts_Formset,form_Accounts)
       
        # older_form_with_data = [form in Older_Freight_PaymentMethod_Accounts_FormSet.forms in form.instance.pk is not None]

        context = {
            'form_Accounts':form_Accounts,
            'older_form_payment_account':Older_PaymentMethod_Accounts_Formset,
            'form_payment_account':PaymentMethod_Accounts_FormSet,
            'frete_form':frete_form,
            'rmn_form':rmn_form,
            'tax_form':tax_form,
            'compra_form': compra_form,
            'compra_item_formset': compra_item_formset
        }
        return render(request, 'purchase/compras_formUpdate.html', context)

@login_required# Deletar uma Compra
@transaction.atomic
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
    messages.success(request,"Compra deletada com sucesso!",extra_tags='successShopping')
    return redirect('compras_list')

@login_required# Criar CompraItem para uma compra específica
@transaction.atomic
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
    search_query = request.GET.get('query', '')
    sort = request.GET.get('sort')
    direction = request.GET.get('dir', 'asc')
   
    if search_query:
        products = Product.objects.filter(
        (
            Q(id__startswith=search_query) |
            Q(description__startswith=search_query) |
            Q(product_code__startswith=search_query)
            ) &
        Q(is_active=True)
        )
    else:
        products = Product.objects.filter(
            is_active=True
        )
    
    paginator = Paginator(products,2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    page_items = list(page.object_list)

    colunas = [
        ('id','ID'),
        ('description','Descrição'),
        ('product_code','Código do Produto'),
        ('selling_price','Preço de Venda')
    ]
    if sort:
        reverse = (direction == 'desc')
        page_items = sorted(page_items,key=attrgetter(sort),reverse=reverse)

    page.object_list = page_items

    # products = Product.objects.filter(is_active=True)
    return render(request, 'purchase/product_list.html', 
        {
            'colunas':colunas,
            'products': page,
            'query':search_query,
            'current_sort':sort,
            'current_dir':direction
         }
    )

@login_required
@transaction.atomic
@permission_required('purchase.add_product', raise_exception=True)
def productForm(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Produto cadastrado com sucesso.",extra_tags='successProduct')
            return redirect('Product')
        else:
            print('Erro no formulário de produto:',form.errors)
    else:
        form = ProductModelForm()
    return render(request, 'purchase/product_form.html', {'form': form})

@login_required
@transaction.atomic
def updateProduct(request, id_product):
    product = get_object_or_404(Product, id=id_product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,"Produto atualizado com sucesso.",extra_tags='successProduct')
            return redirect('Product')
    else:
        form = ProductModelForm(instance=product)
    return render(request, 'purchase/product_form.html', {'form': form})

@login_required
@transaction.atomic
def deleteProduct(request, id_product):
    product = get_object_or_404(Product, id=id_product)
    product.is_active = False
    product.save()
    messages.success(request,"Produto deletado com sucesso.",extra_tags='successProduct')
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

    usuario_paginator = Paginator(products,2)
    page = usuario_paginator.get_page(page_num)

    response_data = {
        'produtos':list(page.object_list),
        'quert':query,
        'pagination':{
            'has_previous': page.has_previous(),
            'previous_page': page.previous_page_number() if page.has_previous() else None,
            'has_next': page.has_next(),
            'next_page': page.next_page_number() if page.has_next() else None,
            'current_page': page.number,
            'total_pages': usuario_paginator.num_pages,
        },
        'message': f"{len(products)} produto(s) encontrado(s)" if page.object_list else "Nenhum produto encontrado"
    }

    return JsonResponse(response_data)

def get_product_id(request):
    query = request.GET.get('query','')
    resultados = Product.objects.filter(
        Q(id=query) 
    )
    resultados_json = list(resultados.values("product_code","description"))
 
   
    return JsonResponse({'produto':resultados_json})

def returnProducts_list(request):
    vendasItens = VendaItem.objects.filter(
        Q(status = 'Entregue')
    )
    workOrders = VendaItemWS.objects.filter(
        Q(status='Entregue')
    )

    all_products_with_status = [
        {'idVenda': vendaItem.venda.id,'idProduto':vendaItem.product.id,'idVendaItem':vendaItem.id,'descricao': vendaItem.product.description, 'quantidade': vendaItem.quantidade, 'status': vendaItem.status,'id':vendaItem.id} for vendaItem in vendasItens
    ] + [
        {'idOS': workOrder.venda.id, 'idProduto':workOrder.product.id,'idVendaItem':workOrder.id,'descricao': workOrder.product.description, 'quantidade': workOrder.quantidade,'status':workOrder.status,'id':workOrder.id} for workOrder in workOrders
    ]
    status_options = ["Pendente", "Entregue"]

    return render(request,'purchase/manageDeliveries_list.html',
        {
            'all_products_with_status': all_products_with_status,
            "status_options": status_options,
            'type':'Entregue'
        }
    )

def expedition_product(request, pk):
    vendaItem = get_object_or_404(VendaItem, id=pk)
    old_quantity_vendaItem = vendaItem.current_quantity  

    if request.method == "POST":
        vendaItemExpeditionForm = VendaItemFormExpedition(request.POST, instance=vendaItem)

        if vendaItemExpeditionForm.is_valid():
            new_quantity_vendaItem = vendaItemExpeditionForm.cleaned_data['current_quantity']
            product = get_object_or_404(Product, pk=vendaItemExpeditionForm.instance.product.id)

            if new_quantity_vendaItem == old_quantity_vendaItem:
                vendaItem.status = 'Entregue'

            vendaItem.current_quantity = old_quantity_vendaItem - int(new_quantity_vendaItem)
            product.current_quantity -= int(new_quantity_vendaItem)

            vendaItem.save()
            product.save()

        else:
            print('Erro no VendaItemExpeditionForm', vendaItemExpeditionForm.errors)

        return redirect('manageProductDelivery')

    else:
        vendaItemExpeditionForm = VendaItemFormExpedition(instance=vendaItem)
        return render(request, "purchase/expeditionProduct_form.html", {
            'vendaItemForm': vendaItemExpeditionForm
        })

def return_product(request, pk):
    vendaItem = get_object_or_404(VendaItem, id=pk)

    if request.method == 'POST':
        vendaItemDevolutedForm = ReturnVendaItemForm(request.POST, instance=vendaItem)
        query = request.POST.get('query', 0)
        direction = request.POST.get('direction', '')

        print("direction:", direction)
        print("query:", query)

        if vendaItemDevolutedForm.is_valid():
            devolvida = vendaItemDevolutedForm.cleaned_data['quantidade']
            # vendaItem.quantidade -= devolvida
            # if vendaItem.quantidade >=1:
            #     vendaItem.save()
            # else:
            #     vendaItem.delete()

            print("Formulário válido")
            if direction == '1':
                print("Direção = 1")
                
                print(f"Nova quantidade: {vendaItem.quantidade}")
                
                pessoa = vendaItem.venda.pessoa
                Credit.objects.create(
                    person=pessoa,
                    credit_data=datetime.now(),
                    credit_value=float(query)
                )
            else:
                # 'Devolução do Produto {product.name} com o valor {product.value} da venda {sale.id}'
                request.session['dados_temp'] = {
                'description': f'Devolução do Produto "{vendaItem.product.description}" de quantidade {vendaItem.quantidade} com o valor total R$ {vendaItem.price_total} da venda de id {vendaItem.venda.id}',
                'person': f'{vendaItem.venda.pessoa}',
                'totalValue':query
                }
                return redirect('Accounts_Create')
        else:
            print("Erro no formulário:", vendaItemDevolutedForm.errors)
    else:
        vendaItemDevolutedForm = ReturnVendaItemForm(instance=vendaItem)

    return render(request, 'purchase/devoluteProduct_form.html', {
        'vendaItemForm': vendaItemDevolutedForm
    })

# def listTableProduct(request):

#     tables = ProductGroup.objects.all()

#     context = {
#         'tables': tables
#     }

#     return render(request, 'purchase/table_list.html', context)


# @permission_required('purchase.view_product', raise_exception=True)
@login_required
def listTablePerson(request):
    sort = request.GET.get('sort')
    direction = request.GET.get('dir', 'asc')
   
    productgroup = NomeGrupoPessoas.objects.all()
    
    paginator = Paginator(productgroup,20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    page_items = list(page.object_list)

    colunas = [
        ('id','ID'),
        ('name_group','Nome do Grupo'),
    ]
    if sort:
        reverse = (direction == 'desc')
        page_items = sorted(page_items,key=attrgetter(sort),reverse=reverse)

    page.object_list = page_items

    # products = Product.objects.filter(is_active=True)
    return render(request, 'purchase/table_list.html', 
        {
            'colunas':colunas,
            'tables': page,
            'current_sort':sort,
            'current_dir':direction
         }
    )

# @login_required
# def tableForm(request):
#     if request.method == "POST":
#         form_person = NomeGrupoPessoasForm(request.POST)
#         formset = NomeGrupoPessoasQuantidadeForm(request.POST)
#         product = ProductGroup.objects.create()
#         if form_person.is_valid(): #and formset.is_valid():
#             grupo = form_person.save()
#             return redirect('listTableProduct')  # redirecione como desejar
#     else:
#         form_person = NomeGrupoPessoasForm()
#         formset = NomeGrupoPessoasQuantidadeForm()
#         # formset = NomeGrupoPessoasQuantidadeFormSet()

#     return render(request, 'purchase/tableForm.html', context={'form':form_person})

@login_required
def tableForm(request):
    NomeGrupoPessoasQuantidadeFormSet = inlineformset_factory(NomeGrupoPessoas, NomeGrupoPessoasQuantidade, fields=['person'], extra=1, can_delete=True)
    ProductGroupFormSet = inlineformset_factory(ProductGroup, ProductPrice, fields=['product_group'], extra=1, can_delete=True)
    if request.method == "POST":
        form = NomeGrupoPessoasForm(request.POST)
        formset = NomeGrupoPessoasQuantidadeFormSet(request.POST)
        formset_products = ProductGroupFormSet(request.POST) 
        if form.is_valid() and formset.is_valid(): #and formset.is_valid():
            if formset_products and formset_products.is_valid():
                for products in formset_products:
                    pass
            grupo = form.save()
            membros = formset.save(commit=False)
            for membro in membros:
                membro.group = grupo
                membro.save()
            return redirect('listTableProduct')  # redirecione como desejar
    else:
        form = NomeGrupoPessoasForm()
        formset = NomeGrupoPessoasQuantidadeFormSet()

    return render(request, 'purchase/tableForm.html', context={'form':form,'formset':formset})

""" preciso que tenha uma tela para cadastrar a tabela, essa tabela tera o nome e o """

@login_required
def updateTable(request, id_table):
    # form = 

    if request.method == "POST":
        pass
    else:
        pass        #coloca os formularios aq 
    return render(request, 'purchase/tableForm.html', context={'form':form})

@login_required
def getTable(request, id_table):
    NomeGrupoPessoasQuantidadeFormSet = inlineformset_factory(NomeGrupoPessoas, NomeGrupoPessoasQuantidade, fields=['person'], extra=1, can_delete=True)

    if request.method == "POST":
        pass
    else:
        pass        #coloca os formularios aq 
    return render(request, 'purchase/tableForm.html', context={'form':form})

@login_required
def deleteTable(request, id_table):
    table = get_object_or_404(ProductGroup, id_table)
    table.delete()
    redirect('listTableProduct')

@login_required
def InactiveTable(request, id_table):
    table = ProductGroup.objects.filter(id=id_table)
    table.is_active = 0
    redirect('listTableProduct')


@login_required
def listTableProduct(request):
    sort = request.GET.get('sort')
    direction = request.GET.get('dir', 'asc')
   
    productgroup = ProductGroup.objects.all()
    
    paginator = Paginator(productgroup,20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    page_items = list(page.object_list)

    colunas = [
        ('id','ID'),
        ('name_group','Nome do Grupo'),
    ]
    if sort:
        reverse = (direction == 'desc')
        page_items = sorted(page_items,key=attrgetter(sort),reverse=reverse)

    page.object_list = page_items

    # products = Product.objects.filter(is_active=True)
    return render(request, 'purchase/table_list.html', 
        {
            'colunas':colunas,
            'tables': page,
            'current_sort':sort,
            'current_dir':direction
         }
    )

@login_required
def tableProductForm(request):
    if request.method == "POST":
        form_product = ProductGroupForm(request.POST)
        if form_product.is_valid(): #and formset.is_valid():
            form_product.save()
            return redirect('listTableProduct')  # redirecione como desejar
    else:
        form_product = ProductGroupForm()

    return render(request, 'purchase/tableForm.html', context={'form':form_product})

def getTableProduct(request, id_tableProduct):
    pass
def updateTableProduct(request, id_tableProduct):
    pass
def deleteTableProduct(request, id_tableProduct):
    pass

 