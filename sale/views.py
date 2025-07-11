from decimal import Decimal
from operator import attrgetter
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
# from registry.forms import SearchForm
from finance.forms import AccountsForm, PaymentMethodAccountsForm, PaymentMethodAccountsReadOnlyForm
from finance.models import CaixaDiario, CashMovement, PaymentMethod_Accounts
from sale.services.sale_service import VendaService
from .forms import *
from .models import *
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Case, When, Value, CharField, F
import platform
from escpos.printer import Serial, Usb, Dummy, File
import sys
### SALE

@login_required
def venda_list(request):
    sort = request.GET.get('sort')
    direction = request.GET.get('dir', 'asc')
    search_query = request.GET.get('query', '')

    # Filtro de busca
    if search_query:
       sales = Venda.objects.annotate(
        nome_cliente=Case(
        When(pessoa__id_FisicPerson_fk__isnull=False, then=F('pessoa__id_FisicPerson_fk__name')),
        When(pessoa__id_LegalPerson_fk__isnull=False, then=F('pessoa__id_LegalPerson_fk__fantasyName')),
        When(pessoa__id_ForeignPerson_fk__isnull=False, then=F('pessoa__id_ForeignPerson_fk__name_foreigner')),
        default=Value(''),
        output_field=CharField()
        ),
        nome_situacao = Case(
        When(situacao__isnull=False,then=F('situacao__name_Situation')),
        default=Value(''),
        output_field=CharField()
        )
        ).filter(
            Q(id__istartswith=search_query) |
            Q(nome_cliente__istartswith=search_query) |
            Q(nome_situacao__istartswith=search_query)
        )
    else:
        sales = Venda.objects.annotate(
        nome_cliente=Case(
        When(pessoa__id_FisicPerson_fk__isnull=False, then=F('pessoa__id_FisicPerson_fk__name')),
        When(pessoa__id_LegalPerson_fk__isnull=False, then=F('pessoa__id_LegalPerson_fk__fantasyName')),
        When(pessoa__id_ForeignPerson_fk__isnull=False, then=F('pessoa__id_ForeignPerson_fk__name_foreigner')),
        default=Value(''),
        output_field=CharField()
        ),
        nome_situacao = Case(
        When(situacao__isnull=False,then=F('situacao__name_Situation')),
        default=Value(''),
        output_field=CharField()
        )).all()

    # Paginar primeiro, sem ordenar ainda
    paginator = Paginator(sales, 2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    # Obter os objetos da página
    page_items = list(page.object_list)

    # Ordenar SOMENTE os itens da página
    foreign_keys = {
        'pessoa':'nome_cliente',
        'situacao':'nome_situacao'
    }

    if sort:
        reverse = (direction == 'desc')
        if sort in foreign_keys:
            value = foreign_keys[sort]
            page_items = sorted(page_items, key=attrgetter(value), reverse=reverse)
        else:
            page_items = sorted(page_items, key=attrgetter(sort), reverse=reverse)
     

    # Substitui os itens da página ordenados
    page.object_list = page_items
    
    colunas = [
        ('id','ID'),
        ('pessoa','Pessoa'),
        ('data_da_venda','Data da Venda'),
        ('situacao','Situação'),
    ]
    situations = Situation.objects.filter(is_Active = True)
    options_situations = Situation.CLOSURE_LEVEL_OPTIONS
    return render(request, 'sale/venda_list.html', {
        'colunas':colunas,
        'vendas': page,
        'query':search_query,
        'current_sort':sort,
        'current_dir':direction,
        'situations':situations,
        'options_situations':options_situations
        # 'form':form
        })

def mudar_situacao(request,pk):
    nova_situacao = request.POST.get('opcao')
    situationObject = get_object_or_404(Situation,pk=nova_situacao)
    venda = get_object_or_404(Venda,pk=pk)
    venda.situacao = situationObject
    if situationObject.closure_level == Situation.CLOSURE_LEVEL_OPTIONS[1][0] or situationObject.closure_level[3][0]:
        caixa = CaixaDiario.objects.filter(
            Q(usuario_responsavel=request.user) & 
            Q(is_Active=1)
            ).first()
        if caixa:
            payment_accounts = PaymentMethod_Accounts.objects.filter(venda=venda)
            for payment_account in payment_accounts:
                payment_account.acc = False
                payment_account.save()

                CashMovement.objects.create(
                    cash = caixa,
                    accounts_in_cash = payment_account,
                    forma_pagamento = payment_account.forma_pagamento,
                    categoria = "venda",
                    
                )
        
            # messages.success(request, 'Caixa Aberto Com Sucesso')
            venda.save() 
            return redirect('venda_list')
        else:
            messages.error(request,'Caixa com este usuário não está aberto!')
            return redirect('venda_list')
    

@login_required
@transaction.atomic 
def venda_create(request):
    VendaItemFormSet = inlineformset_factory(Venda, VendaItem, form=VendaItemForm, extra=1, can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(Venda,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=1,can_delete=True)

    if request.method == 'POST':
        previous_url = request.session.get('previous_page','/')

        venda_form = VendaForm(request.POST)
        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)
        venda_item_formset = VendaItemFormSet(request.POST)

        if venda_form.is_valid() and venda_item_formset.is_valid() and PaymentMethod_Accounts_FormSet.is_valid():

            venda = venda_form.save(commit=False)
           
            venda.situacao  = Situation.objects.filter(closure_level = Situation.CLOSURE_LEVEL_OPTIONS[1][0]).first()
            
            venda_item_formset.instance = venda
            venda_item_formset.save(commit=False)

            PaymentMethod_Accounts_FormSet.instance = venda
            total_payment = 0
            
            venda
            
            for form in PaymentMethod_Accounts_FormSet: 
                if form.cleaned_data:
                    form.acc = None
                    valor = form.cleaned_data['value']
                    total_payment+=valor

                    name_payment = form.cleaned_data["forma_pagamento"]
                    paymentWithCredit = PaymentMethod.objects.filter(
                        name_paymentMethod=name_payment,creditPermission=True
                    )
                    
                    if form.cleaned_data["activeCredit"]:
                        creditos = Credit.objects.filter(person=venda.pessoa).order_by('id')
                        restante_para_descontar = Decimal(venda.value_apply_credit)
                        if creditos:
                            for credito in creditos:
                                if restante_para_descontar <= 0:
                                    break  # nada mais a descontar

                                if credito.credit_value >= restante_para_descontar:
                                    credito.credit_value -= restante_para_descontar
                                    credito.save()
                                    restante_para_descontar = Decimal('0')
                                else:
                                    restante_para_descontar -= credito.credit_value
                                    credito.credit_value = Decimal('0')
                                    credito.save()
                                
            if(total_payment == venda_form.cleaned_data['total_value']):  
                venda.situacao = Situation.objects.filter(
                    closure_level=Situation.CLOSURE_LEVEL_OPTIONS[0][0]
                ).first()
                venda.save()
                venda_item_formset.save()
                PaymentMethod_Accounts_FormSet.save()

                for form in PaymentMethod_Accounts_FormSet.deleted_objects:
                    form.delete()
                    form.save()
                    
                messages.success(request, "Venda cadastrada com sucesso.",extra_tags="successSale")
                return redirect('venda_list')

            if total_payment != venda_form.cleaned_data['total_value']:
                messages.warning(request, "Ação cancelada! O valor não foi salvo completamente.",extra_tags='salecreate_page')
            
            return redirect('venda_create')
           
            
        if not venda_form.is_valid():
            print('Erro no venda_form: ',venda_form.errors)

        if not venda_item_formset.is_valid():
            print("Erro no venda_item_formset: ",venda_item_formset.errors)

        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no PaymentMethod_Accounts_FormSet: ",PaymentMethod_Accounts_FormSet.errors)

    if 'HTTP_REFERER' in request.META:
        request.session['previous_page'] = request.META['HTTP_REFERER']

    form_Accounts = AccountsForm()
    PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
    venda_form = VendaForm()
    venda_item_formset = VendaItemFormSet(queryset=VendaItem.objects.none())

    context = {
        'form_Accounts':form_Accounts,
        'form_payment_account':PaymentMethod_Accounts_FormSet,
        'venda_form': venda_form,       
        'venda_item_formset': venda_item_formset,
    }
    return render(request, 'sale/venda_form.html', context)

@login_required
@transaction.atomic 
def venda_update(request, pk):
    # Carregar a venda existente
    venda = get_object_or_404(Venda, pk=pk)
    
    # Criar formsets para itens de venda e formas de pagamento
    sale,saleItem,payments=VendaService().disabled_fields_based_on_situation(venda.situacao.pk,venda)

    form_class_sale = sale[0]
    permit_edition_sale = sale[1]

    form_class_saleItem = saleItem[0]
    permit_edition_saleItem = saleItem[1]

    form_class_payments = payments[0]
    permit_edition_payment = payments[1]

    VendaItemFormSet = inlineformset_factory(Venda, VendaItem, form=form_class_saleItem, extra=0, can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(
        Venda, 
        PaymentMethod_Accounts, 
        form=form_class_payments, 
        extra=1, 
        can_delete=True)
    OlderPaymentMethodAccountsFormSet = inlineformset_factory(Venda, PaymentMethod_Accounts,form=form_class_payments, extra=0, can_delete=True)

    if request.method == 'POST':
        # previous_url = request.session.get('previous_page','/')
        venda_form = VendaForm(request.POST, instance=venda)
        venda_item_formset = VendaItemFormSet(request.POST, instance=venda)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST,instance=venda,prefix="paymentmethod_accounts_set")
        Older_PaymentMethod_Accounts_FormSet = OlderPaymentMethodAccountsFormSet(request.POST,instance=venda,prefix="older_paymentmethod_accounts_set")
        form_Accounts = AccountsForm(request.POST,instance=venda)   

        if venda_form.is_valid() and venda_item_formset.is_valid() and PaymentMethod_Accounts_FormSet.is_valid() and Older_PaymentMethod_Accounts_FormSet.is_valid():
            venda_form.save(commit=False)

            venda_item_instances = venda_item_formset.save(commit=False) 

            venda_item_formset.save_m2m()  
            itens_para_deletar = []  
        
            for form in venda_item_formset.deleted_forms:
                if form.instance.pk is not None:  
                    itens_para_deletar.append(form.instance)

            pessoa = venda_form.cleaned_data["pessoa"]
            credit = Credit.objects.filter(person=pessoa).order_by('-id').first()
            value_payments = PaymentMethod_Accounts.objects.filter(venda = venda.id,activeCredit=True)

            for value_payment in value_payments:
                credit.credit_value += value_payment.value

            if credit:
                credit.save()
            total_payment = 0
            
            onlyOldPayments = False 
            # venda.value_apply_credit = request.POST.get('credit_value')
            
            if not venda_form.cleaned_data['apply_credit']:
                venda_form.cleaned_data['value_apply_credit'] = 0
            value_new_form = request.POST.get('new_form','').lower()
            has_new_form = value_new_form in ['true', '1', 'on', 'yes']

            if has_new_form:
                onlyOldPayments = False
                for form in PaymentMethod_Accounts_FormSet:
                    if form.cleaned_data:
                        valor = form.cleaned_data['value']
                        if not form.cleaned_data["DELETE"] :
                            total_payment += valor
                        if form.cleaned_data["activeCredit"]:
                            creditos = Credit.objects.filter(person=venda.pessoa).order_by('id')
                            restante_para_descontar = Decimal(venda.value_apply_credit)

                            for credito in creditos:
                                if restante_para_descontar <= 0:
                                    break

                                if credito.credit_value >= restante_para_descontar:
                                    credito.credit_value -= restante_para_descontar
                                    credito.save()
                                    restante_para_descontar = Decimal('0')
                                else:
                                    restante_para_descontar -= credito.credit_value
                                    credito.credit_value = Decimal('0')
                                    credito.save()
            else:
                onlyOldPayments = True
                for form in Older_PaymentMethod_Accounts_FormSet:
                    if form.cleaned_data:
                        valor = form.cleaned_data['value']
                        if not form.cleaned_data["DELETE"] :
                            total_payment += valor

                        if form.cleaned_data["activeCredit"]:
                            creditos = Credit.objects.filter(person=venda.pessoa).order_by('id')
                            restante_para_descontar = Decimal(venda.value_apply_credit)

                            for credito in creditos:
                                if restante_para_descontar <= 0:
                                    break  # nada mais a descontar

                                if credito.credit_value >= restante_para_descontar:
                                    credito.credit_value -= restante_para_descontar
                                    credito.save()
                                    restante_para_descontar = Decimal('0')
                                else:
                                    restante_para_descontar -= credito.credit_value
                                    credito.credit_value = Decimal('0')
                                    credito.save()
          

            if (total_payment == venda_form.cleaned_data['total_value']):

                venda_form.save()
                for instance in venda_item_instances:
                    instance.save() 

                for item in itens_para_deletar:
                    item.delete()
                
                if not onlyOldPayments :

                    if len(PaymentMethod_Accounts_FormSet) >= len(Older_PaymentMethod_Accounts_FormSet):

                        for old_form, new_form in zip(Older_PaymentMethod_Accounts_FormSet, PaymentMethod_Accounts_FormSet):
                            old_instance = old_form.instance
                            new_instance = new_form.instance

                            old_instance.forma_pagamento = new_instance.forma_pagamento
                            old_instance.expirationDate = new_instance.expirationDate
                            old_instance.days = new_instance.days
                            old_instance.value = new_instance.value
                            old_instance.activeCredit = new_instance.activeCredit

                            old_instance.save()

                            new_form.cleaned_data["DELETE"] = True
                        
                        Older_PaymentMethod_Accounts_FormSet.save()
                        PaymentMethod_Accounts_FormSet.save() 
            
                    else:
                    # atualizar os formulários existentes
                        for old_form, new_form in zip(Older_PaymentMethod_Accounts_FormSet, PaymentMethod_Accounts_FormSet):
                            old_instance = old_form.instance
                            new_instance = new_form.instance

                            old_instance.forma_pagamento = new_instance.forma_pagamento
                            old_instance.expirationDate = new_instance.expirationDate
                            old_instance.days = new_instance.days
                            old_instance.value = new_instance.value
                            old_instance.activeCredit = new_instance.activeCredit

                            old_instance.save()

                        # remover os formulários extras de Older_PaymentMethod_Accounts_FormSet
                        for extra_form in Older_PaymentMethod_Accounts_FormSet[len(PaymentMethod_Accounts_FormSet):]:
                            extra_form.instance.delete()

                        Older_PaymentMethod_Accounts_FormSet.save()                            
                else:
                    Older_PaymentMethod_Accounts_FormSet.save()    
                # messages.success(request, "Venda atualizada com sucesso!")
                messages.success(request, "Venda atualizada com sucesso.",extra_tags="successSale")
                return redirect('venda_list')
            
            if total_payment != venda_form.cleaned_data['total_value']:
                messages.warning(request,"Ação cancelada! O valor acumalado dos pagamentos é menor do que o valor acumulado dos prudutos.",extra_tags='vendaupdate_page')

            return redirect('venda_update',pk=pk)
        
        if not venda_form.is_valid():
            print('Erros no venda_form: ',venda_form.errors)

        if not venda_item_formset.is_valid():
            print('Erros no venda_item_formset: ',venda_item_formset.errors)

        if not PaymentMethod_Accounts_FormSet.is_valid():
            print('Erros no PaymentMethod_Accounts_FormSet: ',PaymentMethod_Accounts_FormSet.errors)
        
        if not Older_PaymentMethod_Accounts_FormSet.is_valid():
            print("Erros no Older_PaymentMethod_Accounts_Formset: ",Older_PaymentMethod_Accounts_FormSet.errors)


    venda_form = form_class_sale(instance=venda)
    form_Accounts = AccountsForm(instance=venda)
    Older_PaymentMethod_Accounts_FormSet = OlderPaymentMethodAccountsFormSet(queryset=venda.paymentmethod_accounts_set.all(),instance=venda,prefix='older_paymentmethod_accounts_set')
    PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
    venda_item_formset = VendaItemFormSet(queryset=venda.vendaitem_set.all(),instance=venda)
    
    count_payment = 0

    for i,form in enumerate(Older_PaymentMethod_Accounts_FormSet):
        if i == 0:
            data_obj = form.initial["expirationDate"]  
            data_modificada = data_obj - timedelta(days=int(form.initial["days"])) 
            data_modificada = datetime.strptime(str(data_modificada), "%Y-%m-%d").strftime("%d/%m/%Y") 

        count_payment+=1
    form_Accounts.initial["date_init"] = data_modificada
    form_Accounts.initial["totalValue"] = venda_form.initial['total_value']
    form_Accounts.initial["numberOfInstallments"] = count_payment 

    context = {
            'form_Accounts': form_Accounts,
            'form_payment_account':PaymentMethod_Accounts_FormSet,
            'venda_form': venda_form,
            'venda_item_formset': venda_item_formset,
            'older_form_payment_account':Older_PaymentMethod_Accounts_FormSet,
            'permition_edit_sale':permit_edition_sale,
            'permition_edit_saleItem':permit_edition_saleItem,
            'permition_edit_payments':permit_edition_payment
    }

    return render(request, 'sale/venda_formUpdate.html', context)

@login_required# Deletar uma Venda
@transaction.atomic 
def venda_delete(request, pk):
    # Obtém a venda com base no id (pk)
    venda = get_object_or_404(Venda, pk=pk)
    # Recupera os itens de venda relacionados
    venda_items = VendaItem.objects.filter(venda=venda)
    # Restaura a quantidade dos produtos no estoque
    pessoa = venda.pessoa
    value_payments = PaymentMethod_Accounts.objects.filter(venda = venda.id,activeCredit=True)

    for value_payment in value_payments:
        pessoa.creditLimit+= value_payment.value

    pessoa.save()
    # Exclui os itens de venda
    venda_items.delete()
    # Exclui a venda
    venda.delete()
    messages.success(request, "Venda deletada com sucesso.",extra_tags="successsale")
    # Redireciona para a lista de vendas após a deleção
    return redirect('venda_list')

@login_required# Criar VendaItem para uma venda específica
@transaction.atomic 
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

@login_required
def print_sale_CNF(request, pk):
    venda = Venda.objects.get(id=pk)
    pessoa = venda.pessoa
    endereco = pessoa.id_address_fk
    venda_item = VendaItem.objects.filter(venda=pk)
    forma_pgto = PaymentMethod_Venda.objects.filter(venda=pk)

    context={
        'venda': venda,
        'pessoa': pessoa,
        'endereco': endereco,
        'venda_item': venda_item,
        'forma_pgto': forma_pgto
        }

    return render(request, 'sale/sale.html', context)

@login_required
def client_search(request):
    """Busca clientes dinamicamente e retorna JSON."""
    query = request.GET.get('query', '') 
    resultados = Person.objects.filter(
        (
        Q(id__icontains=query) | 
        Q(id_FisicPerson_fk__name__icontains=query) | 
        Q(id_ForeignPerson_fk__name_foreigner__icontains=query) | 
        Q(id_LegalPerson_fk__fantasyName__icontains=query)
        ) & Q(isClient = True)
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

def supplier_search(request):
    query = request.GET.get('query', '')
    resultados = Person.objects.filter(
        (
            Q(id__icontains=query) | 
            Q(id_FisicPerson_fk__name__icontains=query) | 
            Q(id_ForeignPerson_fk__name_foreigner__icontains=query) | 
            Q(id_LegalPerson_fk__fantasyName__icontains=query)
        ) & Q(isSupllier=True)
    ).order_by('id')[:5]

    # sempre devolva a chave 'fornecedores'
    fornecedores = []
    for supplier in resultados:
        name = (
            supplier.id_FisicPerson_fk.name if supplier.id_FisicPerson_fk else 
            supplier.id_ForeignPerson_fk.name_foreigner if supplier.id_ForeignPerson_fk else 
            supplier.id_LegalPerson_fk.fantasyName if supplier.id_LegalPerson_fk else 
            'Nome não disponível'
        )
        fornecedores.append({'id': supplier.id, 'name': name})

    return JsonResponse({
        'fornecedores': fornecedores,
        'message': 'Nenhum fornecedor encontrado.' if not fornecedores else ''
    })

@login_required
def get_product_id(request):
    query = request.GET.get('query','')
    resultados = Product.objects.filter(
        Q(id=query) 
    )
    resultados_json = list(resultados.values("product_code","description"))
    print(resultados_json)
 
   
    return JsonResponse({'produto':resultados_json})

@login_required
def product_search(request):
    query = request.GET.get('query','')
    resultados = Product.objects.filter(
        (
        Q(product_code__icontains=query) |
        Q(description__icontains=query)
        )
        & Q(is_active = True)
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
        (
            Q(id__istartswith=query) | 
            Q(pessoa__id_FisicPerson_fk__name__istartswith=query) |
            Q(pessoa__id_ForeignPerson_fk__name_foreigner__istartswith=query) |
            Q(pessoa__id_LegalPerson_fk__fantasyName__istartswith=query)
        )
        & Q(is_active = True)
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
        'query':query,
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

def printsale(request, venda_pk=1):
    venda_list = Venda.objects.get(id=venda_pk)
    venda_item = VendaItem.objects.filter(venda=venda_list.id)
    # print(vars(venda_list))
    print(vars(venda_item))
    context = {
        'venda': venda_list,
        'venda_item': venda_item,
    }
    return render(request, 'sale/sale.html', context)

    # # Carregar a venda existente
    # venda = get_object_or_404(Venda, pk=venda_pk)

    # # Criar formsets para itens de venda e formas de pagamento
    # VendaItemFormSet = inlineformset_factory(Venda, VendaItem, form=VendaItemForm, extra=0, can_delete=True)
    # PaymentMethodVendaFormSet = inlineformset_factory(Venda, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=0, can_delete=True)

    # form_Accounts = AccountsForm(instance=venda)
    # venda_form = VendaForm(instance=venda)
    # payment_method_formset = PaymentMethodVendaFormSet(queryset=venda.paymentmethod_accounts_set.all(),instance=venda)
    # venda_item_formset = VendaItemFormSet(queryset=venda.vendaitem_set.all(),instance=venda)

    # context = {
    #     'form_Accounts': form_Accounts,
    #     'venda_form': venda_form,
    #     'venda_item_formset': venda_item_formset,
    #     'form_payment_account': payment_method_formset,
    # }
