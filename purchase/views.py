
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.db.models.functions import Coalesce
from django.db.models import F, Value
from Sale.models import Venda, VendaItem

from Service.models import VendaItem as VendaItemWS
from .forms import *
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from finance.models import Freight_PaymentMethod_Accounts, PaymentMethod_Accounts, Romaneio_PaymentMethod_Accounts, Tax_PaymentMethod_Accounts
from finance.forms import FreightPaymentMethod_AccountsForm, PaymentMethodAccountsForm, AccountsForm, RomaneioPaymentMethod_AccountsForm, TaxPaymentMethodAccountsForm
from django.db import transaction

### PURCHASE

@login_required
def productsWithStatus_list(request):
    vendasItens = VendaItem.objects.filter(
        Q(status = 'Pendente')
    )
    workOrders = VendaItemWS.objects.filter(
        Q(status = 'Pendente')
    )
    status_options = ["Pendente", "Entregue"]

    all_products_with_status = [
        {'idVenda': vendaItem.venda.id,'idProduto':vendaItem.product.id,'idVendaItem':vendaItem.id,'descricao': vendaItem.product.description, 'quantidade': vendaItem.quantidade, 'status': vendaItem.status} for vendaItem in vendasItens
    ] + [
        {'idOS': workOrder.venda.id, 'idProduto':workOrder.product.id,'idVendaItem':workOrder.id,'descricao': workOrder.product.description, 'quantidade': workOrder.quantidade,'status':workOrder.status} for workOrder in workOrders
    ]
    # messages.warning(request,'TESTE',extra_tags='delivery_page')
    return render(request, 'purchase/manageDeliveries_list.html', {
        'all_products_with_status': all_products_with_status,
        "status_options": status_options

    })

@login_required
@transaction.atomic
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
        total_payment = 0   
        for form in paymentForm:
            if form.cleaned_data:
                form.instance.acc = True
                valor = form.cleaned_data['value']
                total_payment+=valor
        return total_payment
    
    def savePayments(paymentForm):
        for form in paymentForm:
            conta = form.save(commit=False)  # cria o objeto sem salvar ainda
            conta.compra = compra            # agora sim associa corretamente
            conta.acc = True
            conta.save()  
    
    CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=1, can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    TaxPaymentMethodAccountsFormSet = inlineformset_factory(Compra,Tax_PaymentMethod_Accounts,form=TaxPaymentMethodAccountsForm,extra=1,can_delete=True)
    FreightPaymentMethodAccountsFormSet = inlineformset_factory(Compra,Freight_PaymentMethod_Accounts,form=FreightPaymentMethod_AccountsForm,extra=1,can_delete=True)
    RomaneioPaymentMethodAccountsFormSet = inlineformset_factory(Compra,Romaneio_PaymentMethod_Accounts,form=RomaneioPaymentMethod_AccountsForm,extra=1,can_delete=True)

    if request.method == 'POST':
        
        compra_form = CompraForm(request.POST)

        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)

        tax_form_Accounts = AccountsForm(request.POST,prefix='tax_form_accounts')
        TaxPaymentMethod_Accounts_FormSet = TaxPaymentMethodAccountsFormSet(request.POST)

        freight_form_Accounts = AccountsForm(request.POST,prefix='freight_form_accounts')
        FreightPaymentMethod_Accounts_FormSet = FreightPaymentMethodAccountsFormSet(request.POST)

        romaneio_form_Accounts = AccountsForm(request.POST,prefix='romaneio_form_accounts')
        RomaneioPaymentMethod_Accounts_FormSet = RomaneioPaymentMethodAccountsFormSet(request.POST)

        compra_item_formset = CompraItemFormSet(request.POST)
        
        if (
            compra_form.is_valid() and 
            compra_item_formset.is_valid() and 
            PaymentMethod_Accounts_FormSet.is_valid() and 
            TaxPaymentMethod_Accounts_FormSet.is_valid() and 
            FreightPaymentMethod_Accounts_FormSet.is_valid() and
            RomaneioPaymentMethod_Accounts_FormSet.is_valid()
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
            total_payment = calculateValuePayments(PaymentMethod_Accounts_FormSet)

            TaxPaymentMethod_Accounts_FormSet.instance = compra
            taxTotal_payment = calculateValuePayments(TaxPaymentMethod_Accounts_FormSet)
            tax_totalValue = compra.total_value - compra.total_value * (Decimal(compra.tax_value) / Decimal('100'))

            freightFOB = False
            equalValueFreight = False
            if compra.freight_type == "fob":
                freightFOB = True
                FreightPaymentMethod_Accounts_FormSet.instance = compra
                freightTotal_payment = calculateValuePayments(FreightPaymentMethod_Accounts_FormSet)
                if compra.freight_value == freightTotal_payment:
                    equalValueFreight = True
            else:
                compra.freight_value = 0
            
            RomaneioPaymentMethod_Accounts_FormSet.instance = compra
            romaneioTotal_payment = calculateValuePayments(RomaneioPaymentMethod_Accounts_FormSet)
            # Verificar se os pagamentos somam corretamente antes de salvar
            if total_payment == compra.total_value and taxTotal_payment == tax_totalValue and romaneioTotal_payment == compra.value_picking_list:
                if freightFOB and equalValueFreight:
                    compra_form.save()
                    compra_item_formset.save()
                    # PaymentMethod_Accounts_FormSet.save()
                    # for form in PaymentMethod_Accounts_FormSet:
                    #     conta = form.save(commit=False)  # cria o objeto sem salvar ainda
                    #     conta.compra = compra            # agora sim associa corretamente
                    #     conta.acc = True
                    #     conta.save()  
                    
                    savePayments(PaymentMethod_Accounts_FormSet)
                    savePayments(TaxPaymentMethod_Accounts_FormSet)
                    savePayments(FreightPaymentMethod_Accounts_FormSet)
                    savePayments(RomaneioPaymentMethod_Accounts_FormSet)

                    messages.success(request,"Compra cadastrada com sucesso.",extra_tags='successShopping')
                    return redirect('compras_list')
                
                elif not freightFOB and not equalValueFreight:
                    compra_form.save()
                    compra_item_formset.save()
                    
                    savePayments(PaymentMethod_Accounts_FormSet)
                    savePayments(TaxPaymentMethod_Accounts_FormSet)
                    savePayments(RomaneioPaymentMethod_Accounts_FormSet)

                    messages.success(request,"Compra cadastrada com sucesso.",extra_tags='successShopping')
                    return redirect('compras_list')
                else:
                    messages.warning(request,"Ação cancelada! O valor total de pagamentos sobre frete FOB não corresponde ao total do frete")
            else:
                messages.warning(request, "Ação cancelada! O valor total dos pagamentos não corresponde ao total da compra.")
        if not compra_form.is_valid():
            print("Erro no CompraForm",compra_form.errors)

        if not compra_item_formset.is_valid():
            print("Erro no CompraItem",compra_item_formset.errors)

        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no PaymentMethod",PaymentMethod_Accounts_FormSet.errors)
        
        if not TaxPaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no TaxPaymentMethod",TaxPaymentMethod_Accounts_FormSet.errors)

        if not FreightPaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no FreightPaymentMethod",FreightPaymentMethod_Accounts_FormSet.errors)

        if not RomaneioPaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no RomaneioPaymentMethod",RomaneioPaymentMethod_Accounts_FormSet.errors)
        # compra_form = CompraForm()
        # compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
        # payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Accounts.objects.none())

    else:
        form_Accounts = AccountsForm()
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())

        tax_form_Accounts = AccountsForm(prefix='tax_form_accounts')
        TaxPaymentMethod_Accounts_FormSet = TaxPaymentMethodAccountsFormSet(queryset=Tax_PaymentMethod_Accounts.objects.none())

        freight_form_Accounts = AccountsForm(prefix='freight_form_accounts')
        FreightPaymentMethod_Accounts_FormSet = FreightPaymentMethodAccountsFormSet(queryset=Freight_PaymentMethod_Accounts.objects.none())

        RomaneioPaymentMethod_Accounts_FormSet = RomaneioPaymentMethodAccountsFormSet(queryset=Romaneio_PaymentMethod_Accounts.objects.none())
        romaneio_form_Accounts =AccountsForm(prefix='romaneio_form_accounts')
        
        compra_form = CompraForm()
        compra_item_formset = CompraItemFormSet(queryset=CompraItem.objects.none())
       
        # payment_method_formset = PaymentMethodCompraFormSet(queryset=PaymentMethod_Accounts.objects.none())

    context = {
        'form_Accounts': form_Accounts,
        'form_payment_account': PaymentMethod_Accounts_FormSet,
        'taxform_Accounts':tax_form_Accounts,
        'form_tax_payment_account':TaxPaymentMethod_Accounts_FormSet,
        'freightform_Accounts':freight_form_Accounts,
        'form_freight_payment_account':FreightPaymentMethod_Accounts_FormSet,
        'romaneioform_Accounts':romaneio_form_Accounts,
        'form_romaneio_payment_account':RomaneioPaymentMethod_Accounts_FormSet,
        'compra_form': compra_form,
        'compra_item_formset': compra_item_formset,
        # 'payment_method_formset': payment_method_formset
    }
    return render(request, 'purchase/compras_form.html', context)

@login_required
@transaction.atomic 
def compras_update(request, pk):
    # TEM QUE MELHORAR ESSA FUNCAO DEPOIS CABEÇAO
    def calculate_value_payments_update(paymentForm,olderPaymentForm):
            try:
                total_payment = 0
                onlyOldPayments = False
                for form in paymentForm:
                    if form.cleaned_data:
                        if not form.cleaned_data.get("DELETE"):
                            valor = form.cleaned_data['value']
                            total_payment += valor
                    else:
                        total_payment = 0
                        onlyOldPayments = True
                        for form in olderPaymentForm:
                            if form.cleaned_data:
                                if not form.cleaned_data['DELETE']:
                                    valor = form.cleaned_data['value']
                                    print(form.cleaned_data['value'])
                                    total_payment+=valor
                                    
            except (TypeError, ValueError, InvalidOperation):
                total_payment = 0
                onlyOldPayments = True
                for form in olderPaymentForm:
                    if form.cleaned_data:
                        if not form.cleaned_data['DELETE']:
                            valor = form.cleaned_data['value']
                            total_payment+=valor
            return total_payment,onlyOldPayments
    
    def rearrange_payments(onlyOldPayments, paymentForm, olderPaymentForm):
        if not onlyOldPayments:
            if len(paymentForm) >= len(olderPaymentForm):
                for old_form, new_form in zip(olderPaymentForm, paymentForm):
                    old_instance = old_form.instance
                    new_instance = new_form.instance

                    old_instance.forma_pagamento = new_instance.forma_pagamento
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
        form_Payment_Accounts.initial["totalValue"] = value_total_payment
        form_Payment_Accounts.initial["numberOfInstallments"] = count_payment

        return form_Payment_Accounts
    # Recupera a instância da Compra existente
    compra = get_object_or_404(Compra, pk=pk)

    CompraItemFormSet = inlineformset_factory(Compra, CompraItem, form=CompraItemForm, extra=0, can_delete=True)

    PaymentMethodAccountsFormSet = inlineformset_factory(Compra, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=1, can_delete=True)
    Older_PaymentMethod_Accounts_Formset = inlineformset_factory(Compra,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=0,can_delete=True)

    TaxPaymentMethodAccountsFormSet = inlineformset_factory(Compra,Tax_PaymentMethod_Accounts,form=TaxPaymentMethodAccountsForm,extra=1,can_delete=True)
    Older_Tax_PaymentMethod_Accounts_Formset = inlineformset_factory(Compra,Tax_PaymentMethod_Accounts,form=TaxPaymentMethodAccountsForm,extra=0,can_delete=True)

    FreightPaymentMethodAccountsFormSet = inlineformset_factory(Compra,Freight_PaymentMethod_Accounts,form=FreightPaymentMethod_AccountsForm,extra=1,can_delete=True)
    Older_Freight_PaymentMethod_Accounts_Formset = inlineformset_factory(Compra,Freight_PaymentMethod_Accounts,form=FreightPaymentMethod_AccountsForm,extra=0,can_delete=True)

    RomaneioPaymentMethodAccountsFormSet = inlineformset_factory(Compra,Romaneio_PaymentMethod_Accounts,form=RomaneioPaymentMethod_AccountsForm,extra=1,can_delete=True)
    Older_Romaneio_PaymentMethod_Accounts_Formset = inlineformset_factory(Compra,Romaneio_PaymentMethod_Accounts,form=RomaneioPaymentMethod_AccountsForm,extra=0,can_delete=True)
    if request.method == 'POST':
        # print(request.POST)
        # Recupera os dados do formulário de compra e formsets de itens e métodos de pagamento
        compra_form = CompraForm(request.POST, instance=compra)
        compra_item_formset = CompraItemFormSet(request.POST, instance=compra)

        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST,instance=compra)
        Older_PaymentMethod_Accounts_FormSet = Older_PaymentMethod_Accounts_Formset(request.POST,instance=compra,prefix="older_paymentmethod_accounts_set")

        TaxPaymentMethod_Accounts_FormSet = TaxPaymentMethodAccountsFormSet(request.POST,instance=compra,prefix="tax_form_payment_account_set")
        Older_Tax_PaymentMethod_Accounts_FormSet = Older_Tax_PaymentMethod_Accounts_Formset(request.POST,instance=compra,prefix="older_tax_form_payment_account_set")
        
        FreightPaymentMethod_Accounts_FormSet = FreightPaymentMethodAccountsFormSet(request.POST,instance=compra,prefix="freight_form_payment_account_set")
        Older_Freight_PaymentMethod_Accounts_FormSet = Older_Freight_PaymentMethod_Accounts_Formset(request.POST,instance=compra,prefix="older_freight_form_payment_account_set")

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
            produto.save()

        compraitems_excluir.delete()
        if (
            compra_form.is_valid() and 
            compra_item_formset.is_valid() and 
            PaymentMethod_Accounts_FormSet.is_valid() and 
            Older_PaymentMethod_Accounts_FormSet.is_valid() and 
            TaxPaymentMethod_Accounts_FormSet.is_valid() and 
            Older_Tax_PaymentMethod_Accounts_FormSet.is_valid() and 
            FreightPaymentMethod_Accounts_FormSet.is_valid() and 
            Older_Freight_PaymentMethod_Accounts_FormSet.is_valid()
            ):
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
            
            total_payment,onlyOldPayments = calculate_value_payments_update(PaymentMethod_Accounts_FormSet,Older_PaymentMethod_Accounts_FormSet)
            taxTotalPayment,onlyTaxOldPayments = calculate_value_payments_update(TaxPaymentMethod_Accounts_FormSet,Older_Tax_PaymentMethod_Accounts_FormSet)
            tax_totalValue = compra_form.cleaned_data['total_value'] - compra_form.cleaned_data['total_value']*(Decimal(compra_form.cleaned_data['tax_value'])/Decimal('100'))


            freightFOB = False
            equalValueFreight = False
            if compra_form.cleaned_data['freight_type'] == 'fob':
                freightFOB = True
                freightTotalPayment,onlyFreightPayments = calculate_value_payments_update(FreightPaymentMethod_Accounts_FormSet,Older_Freight_PaymentMethod_Accounts_FormSet)
                if compra_form.cleaned_data['freight_value'] == freightTotalPayment:
                    equalValueFreight = True 
            else:
                compra_form.cleaned_data['freight_value'] = 0

            if total_payment == compra_form.cleaned_data['total_value'] and taxTotalPayment == tax_totalValue:
                if freightFOB and equalValueFreight:
                    compra_form.save()

                    for instance in compra_item_instances:
                        instance.save()

                    for item in itens_para_deletar:
                        item.delete()
                    
                    rearrange_payments(onlyOldPayments,PaymentMethod_Accounts_FormSet,Older_PaymentMethod_Accounts_FormSet)
                    rearrange_payments(onlyTaxOldPayments,TaxPaymentMethod_Accounts_FormSet,Older_Tax_PaymentMethod_Accounts_FormSet)
                    rearrange_payments(onlyFreightPayments,FreightPaymentMethod_Accounts_FormSet,Older_Freight_PaymentMethod_Accounts_FormSet)

                    messages.success(request,"Compra atualizada com sucesso!",extra_tags='successShopping')
                    return redirect('compras_list')
                
                elif not freightFOB and not equalValueFreight:
                    compra_form.save()

                    for instance in compra_item_instances:
                        instance.save()

                    for item in itens_para_deletar:
                        item.delete()
                    
                    rearrange_payments(onlyOldPayments,PaymentMethod_Accounts_FormSet,Older_PaymentMethod_Accounts_FormSet)
                    rearrange_payments(onlyTaxOldPayments,TaxPaymentMethod_Accounts_FormSet,Older_Tax_PaymentMethod_Accounts_FormSet)
                    Older_Freight_PaymentMethod_Accounts_FormSet.save()

                    messages.success(request,"Compra atualizada com sucesso!",extra_tags='successShopping')
                    return redirect('compras_list')
            if total_payment != compra_form.cleaned_data["total_value"]:
                messages.warning(request, "Ação cancelada! O valor total dos pagamentos não corresponde ao total da compra.")
        
        if not compra_form.is_valid():
            print('Erro no CompraForms', compra_form.errors)

        if not compra_item_formset.is_valid():
            print("Erro no CompraItem",compra_item_formset.errors)
            
        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro na PaymentMethod_Accounts_FormSet",PaymentMethod_Accounts_FormSet.errors)
        
        if not Older_PaymentMethod_Accounts_FormSet.is_valid():
            print('Erro no Older_PaymentMethod_Accounts_FormSet',Older_PaymentMethod_Accounts_FormSet.errors)
        
        if not TaxPaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no TaxPaymentMethod_Accounts_FormSet",TaxPaymentMethod_Accounts_FormSet.errors)
        
        if not Older_Tax_PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no Older_Tax_PaymentMethod_Accounts_FormSet",Older_Tax_PaymentMethod_Accounts_FormSet.errors)
    else:
        # Se for um GET, inicializa o formulário com os dados da compra existente
        form_Accounts = AccountsForm(instance=compra)
        Older_PaymentMethod_Accounts_Formset = Older_PaymentMethod_Accounts_Formset(queryset=compra.paymentmethod_accounts_set.all(),instance=compra,prefix="older_paymentmethod_accounts_set")
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())

        tax_form_Accounts = AccountsForm(instance = compra,prefix='tax_form_accounts')
        Older_Tax_PaymentMethod_Accounts_Formset = Older_Tax_PaymentMethod_Accounts_Formset(queryset=compra.tax_paymentmethod_accounts_set.all(),instance=compra,prefix='older_tax_form_payment_account_set')
        TaxPaymentMethod_Accounts_FormSet = TaxPaymentMethodAccountsFormSet(queryset=Tax_PaymentMethod_Accounts.objects.none(),prefix="tax_form_payment_account_set")

        freight_form_Accounts = AccountsForm(prefix='freight_form_accounts')
        Older_Freight_PaymentMethod_Accounts_FormSet = Older_Freight_PaymentMethod_Accounts_Formset(queryset=compra.freight_paymentmethod_accounts_set.all(),instance=compra,prefix='older_freight_form_payment_account_set')
        FreightPaymentMethod_Accounts_FormSet = FreightPaymentMethodAccountsFormSet(queryset=Freight_PaymentMethod_Accounts.objects.none(),prefix="freight_form_payment_account_set")

        romaneio_form_Accounts = AccountsForm(prefix='romaneio_form_accounts')
        Older_Romaneio_PaymentMethod_Accounts_FormSet = Older_Romaneio_PaymentMethod_Accounts_Formset(queryset=compra.romaneio_paymentmethod_accounts_set.all(),instance=compra,prefix='older_romaneio_form_payment_account_set')
        RomaneioPaymentMethod_Accounts_FormSet = RomaneioPaymentMethodAccountsFormSet(queryset=Romaneio_PaymentMethod_Accounts.objects.none(),prefix="romaneio_form_payment_account_set")

        compra_form = CompraForm(instance=compra)
        compra_item_formset = CompraItemFormSet(queryset=compra.compraitem_set.all(), instance=compra)
        
        
        form_Accounts = populate_account_form(Older_PaymentMethod_Accounts_Formset,form_Accounts)
        tax_form_Accounts = populate_account_form(Older_Tax_PaymentMethod_Accounts_Formset,tax_form_Accounts)
        romaneio_form_Accounts = populate_account_form(Older_Romaneio_PaymentMethod_Accounts_FormSet,romaneio_form_Accounts)
        # older_form_with_data = [form in Older_Freight_PaymentMethod_Accounts_FormSet.forms in form.instance.pk is not None]
        print(len(Older_Freight_PaymentMethod_Accounts_FormSet))
       
        if len(Older_Freight_PaymentMethod_Accounts_FormSet) != 0:
            freight_form_Accounts = populate_account_form(Older_Freight_PaymentMethod_Accounts_FormSet,freight_form_Accounts)

        context = {
            'form_Accounts':form_Accounts,
            'taxform_Accounts':tax_form_Accounts,
            'freightform_Accounts':freight_form_Accounts,
            'romaneioform_Accounts':romaneio_form_Accounts,
            'older_form_payment_account':Older_PaymentMethod_Accounts_Formset,
            'form_payment_account':PaymentMethod_Accounts_FormSet,
            'older_tax_form_payment_account':Older_Tax_PaymentMethod_Accounts_Formset,
            'form_tax_payment_account':TaxPaymentMethod_Accounts_FormSet,
            'older_freight_form_payment_account':Older_Freight_PaymentMethod_Accounts_FormSet,
            'form_freight_payment_account':FreightPaymentMethod_Accounts_FormSet,
            'older_romaneio_form_payment_account':Older_Romaneio_PaymentMethod_Accounts_FormSet,
            'form_romaneio_payment_account':RomaneioPaymentMethod_Accounts_FormSet,
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
    products = Product.objects.filter(is_active=True)
    return render(request, 'purchase/product_list.html', {'products': products})

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