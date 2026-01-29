
from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from finance.forms import AccountsForm, PaymentMethodAccountsForm,PaymentMethodFormSet
from finance.models import CaixaDiario, CashMovement, PaymentMethod_Accounts
from service.services.wo_service import WorkOrderService
from .forms import *
from .models import *
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db import transaction


@login_required
def print_OS_CNF(request, pk):
    os = Vendaservice.objects.get(id=pk)
    pessoa = os.pessoa
    endereco = pessoa.id_address_fk
    os_item = VendaItemservice.objects.filter(os=pk)
    forma_pgto = PaymentMethod_Vendaservice.objects.filter(os=pk)

    context={
        'os': os,
        'pessoa': pessoa,
        'endereco': endereco,
        'os_item': os_item,
        'forma_pgto': forma_pgto
        }

    return render(request, 'os.html', context)

@login_required
@transaction.atomic 
def workOrders_create(request):
    serviceItemFormSet  = inlineformset_factory(Vendaservice,VendaItemservice,form=VendaItemserviceForm,extra=1,can_delete=True)
    VendaItemFormSet = inlineformset_factory(Vendaservice, VendaItem, form=VendaItemForm, extra=1, can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(Vendaservice,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=1,can_delete=True)
    
    if(request.method == 'POST'):
        service_form = VendaserviceForm(request.POST)
        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)
        service_item_formset = serviceItemFormSet(request.POST)
        venda_item_formset = VendaItemFormSet(request.POST)

        if(service_form.is_valid() and venda_item_formset.is_valid() and service_item_formset.is_valid() and PaymentMethod_Accounts_FormSet.is_valid()):
            service = service_form.save(commit=False)

            venda_item_formset.instance = service
            venda_item_formset.save(commit=False)

            service_item_formset.instance = service
            service_item_formset.save(commit=False)

            PaymentMethod_Accounts_FormSet.instance = service
            total_payment = 0
           
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
                        creditos = Credit.objects.filter(person=service.pessoa).order_by('id')
                        restante_para_descontar = Decimal(service.value_apply_credit)
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
                                
            pessoa = service_form.cleaned_data["pessoa"]


            if(total_payment==service.total_value + service.total_value_service) :
               
                pessoa.save()

                service.situacao = Situation.objects.filter(
                    closure_level=Situation.CLOSURE_LEVEL_OPTIONS[0][0]
                ).first()
                service.save()
                venda_item_formset.save()
                service_item_formset.save()

                PaymentMethod_Accounts_FormSet.save()

                for form in PaymentMethod_Accounts_FormSet.deleted_objects:
                    form.delete()
                    form.save()

                messages.success(request,"Ordem de Serviço cadastrada com sucesso.",extra_tags="successWorkOrder")
                return redirect('workOrders_list')
            
            if total_payment != service.total_value:
                messages.warning(request,"Ação cancelada! O valor acumalado dos pagamentos é menor do que o valor acumulado dos prudutos.",extra_tags='workcreate_page')

        
        if not service_form.is_valid():
            print("Erro no serviceForm",service_form.errors)

        if not venda_item_formset.is_valid():
            print("Erro na VendaItem",venda_item_formset.errors)
            
        if not service_item_formset.is_valid():
            print("Erro no VendaserviceItem",service_item_formset.errors)

        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no VendaPagamentoservice",PaymentMethod_Accounts_FormSet.errors)

        return redirect('workOrdersForm')
       
    else:
        form_Accounts = AccountsForm()
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        service_form = VendaserviceForm()
        service_item_formset = serviceItemFormSet(queryset=VendaItemservice.objects.none())
        venda_item_formset = VendaItemFormSet(queryset=VendaItem.objects.none())

        # payment_method_formset = PaymentMethodServiceFormSet(queryset=PaymentMethod_VendaService.objects.none())
    context = {
        'form_Accounts':form_Accounts,
        'form_payment_account':PaymentMethod_Accounts_FormSet,
        'service_form':service_form,
        'service_item_formset':service_item_formset,
        'venda_item_formset':venda_item_formset
        # 'payment_method_formset':payment_method_formset
    }

    return render(request,'workOrders_form.html',context)

@login_required    
@transaction.atomic 
def workOrders_update(request,pk):

    servico = get_object_or_404(Vendaservice, pk=pk)

    sale,saleItem,payments,saleService = WorkOrderService().disabled_fields_based_on_situation(servico.situacao.pk,servico)
    form_class_sale = sale[0]
    permit_edition_sale = sale[1]

    form_class_saleItem = saleItem[0]
    permit_edition_saleItem = saleItem[1]

    form_class_saleService = saleService[0]
    permit_edition_saleService = saleService[1]

    form_class_payments = payments[0]
    permit_edition_payment = payments[1]

    ServiceItemFormSet  = inlineformset_factory(Vendaservice,VendaItemservice,form=form_class_saleService,extra=0,can_delete=True)
    VendaItemFormSet = inlineformset_factory(Vendaservice, VendaItem, form=form_class_saleItem, extra=0, can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(Vendaservice,PaymentMethod_Accounts,form=form_class_payments,extra=1,can_delete=True)
    OlderPaymentMethodAccountsFormSet = inlineformset_factory(Vendaservice, PaymentMethod_Accounts, form=form_class_payments, extra=0, can_delete=True)
    if request.method == 'POST':
        # previous_url = request.session.get('previous_page','/')
        # print(request.POST)
        service_form = VendaserviceForm(request.POST, instance=servico)
        service_item_formset = ServiceItemFormSet(request.POST, instance=servico)
        venda_item_formset = VendaItemFormSet(request.POST,instance=servico)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST, instance=servico,prefix="paymentmethod_accounts_set")
        Older_PaymentMethod_Accounts_FormSet = OlderPaymentMethodAccountsFormSet(request.POST,instance=servico,prefix="older_paymentmethod_accounts_set")
        form_Accounts = AccountsForm(request.POST,instance=servico)

        venda_item = VendaItem.objects.filter(servico=servico)
        ids_existentes_venda_itens = set(venda_item.values_list('id',flat=True))
        ids_enviados_venda_itens = set(
            int(value) for key, value in request.POST.items() 
            if key.startswith("vendaitem_set-") and key.endswith("-id") and value.isdigit()
            )
        ids_para_excluir_venda_itens = ids_existentes_venda_itens - ids_enviados_venda_itens
        VendaItem.objects.filter(id__in=ids_para_excluir_venda_itens).delete()
        

        venda_service_item = VendaItemservice.objects.filter(service=servico.id)
        ids_existentes_venda_service_itens = set(venda_service_item.values_list('id',flat=True))
        ids_enviados_vendas_service_itens = set(
             int(value) for key, value in request.POST.items() 
            if key.startswith("vendaitemservice_set-") and key.endswith("-id") and value.isdigit()
        )
        ids_para_excluir_venda_service_itens = ids_existentes_venda_service_itens - ids_enviados_vendas_service_itens
        VendaItemservice.objects.filter(id__in=ids_para_excluir_venda_service_itens).delete()


        if(
            service_form.is_valid() and 
            venda_item_formset.is_valid() and 
            service_item_formset.is_valid() and
            PaymentMethod_Accounts_FormSet.is_valid() and 
            Older_PaymentMethod_Accounts_FormSet.is_valid() 
            ):
            service = service_form.save(commit=False)

            service_item_instances = service_item_formset.save(commit=False)
            service_item_formset.save_m2m()
            itens_de_servico_para_deletar = []
            for form in service_item_formset.deleted_forms:
                if form.instance.pk is not None:
                    itens_de_servico_para_deletar.append(form.instance)


            venda_item_instances = venda_item_formset.save(commit=False) 
            venda_item_formset.save_m2m() 
            itens_para_deletar = [] 
            for form in venda_item_formset.deleted_forms:
                if form.instance.pk is not None:  
                    itens_para_deletar.append(form.instance)

           

            total_payment = 0
            pessoa = service_form.cleaned_data["pessoa"]
            credit = Credit.objects.filter(person=pessoa).order_by('-id').first()
            value_payments = PaymentMethod_Accounts.objects.filter(venda = servico.id,activeCredit=True)

            for value_payment in value_payments:
                credit.credit_value += value_payment.value

            if not service_form.cleaned_data['apply_credit']:
                service_form.cleaned_data['value_apply_credit'] = 0
            if credit:
                credit.save()
            
            onlyOldPayments = False 
            # valor_usado = request.POST.get('credit_value')
            
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
                            creditos = Credit.objects.filter(person=service.pessoa).order_by('id')
                            restante_para_descontar = Decimal(service.value_apply_credit)

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
                            creditos = Credit.objects.filter(person=service.pessoa).order_by('id')
                            restante_para_descontar = Decimal(service.value_apply_credit)

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
            if (total_payment == service.total_value + service.total_value_service):

                service.save()

                for instance in venda_item_instances:
                    instance.save() 

                for item in itens_para_deletar:
                    item.delete()
                
                
                for instance in service_item_instances:
                    instance.save()

                for item in itens_de_servico_para_deletar:
                    item.delete()

                if not onlyOldPayments:

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
                    # FALTA VERIFICAR ESSA
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
            
                messages.success(request,"Ordem de Serviço atualizada com sucesso.",extra_tags="successWorkOrder")
                return redirect('workOrders_list')
            
            if total_payment != service.total_value + service.total_value_service:
                messages.warning(request,"Ação cancelada! O valor acumalado dos pagamentos é menor do que o valor acumulado dos prudutos.",extra_tags='workupdate_page')
            
            
            return redirect('workOrdersUpdate', pk=pk)

        if not service_form.is_valid():
            print("Erro no serviceForm",service_form.errors)

        if not venda_item_formset.is_valid():
            print("Erro no VendaItem",venda_item_formset.errors)

        if not service_item_formset.is_valid():
            print("Erro no VendaserviceItem",service_item_formset.errors)
            
        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no VendaPagamentoservice",PaymentMethod_Accounts_FormSet.errors)
        
        if not Older_PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no Older_PaymentMethod_Accounts_FormSet",Older_PaymentMethod_Accounts_FormSet.errors)
        
    
    form_Accounts = AccountsForm(instance=servico)
    Older_PaymentMethod_Accounts_FormSet = OlderPaymentMethodAccountsFormSet(queryset=servico.paymentmethod_accounts_set.all(),instance=servico,prefix='older_paymentmethod_accounts_set')
    PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
    service_form = form_class_sale(instance=servico)
    venda_item_formset = VendaItemFormSet(queryset=servico.vendaitem_set.all(),instance=servico)
    service_item_formset = ServiceItemFormSet(queryset = servico.vendaitemservice_set.all(),instance=servico)
    
    count_payment = 0
    
    for i,form in enumerate(Older_PaymentMethod_Accounts_FormSet):
        if i == 0:
            data_obj = form.initial["expirationDate"]  
            data_modificada = data_obj - timedelta(days=int(form.initial["days"])) 
            data_modificada = datetime.strptime(str(data_modificada), "%Y-%m-%d").strftime("%d/%m/%Y") 

        count_payment+=1
    form_Accounts.initial["date_init"] = data_modificada
    form_Accounts.initial["totalValue"] = service_form.initial['total_value'] + service_form.initial['total_value_service']
    form_Accounts.initial["numberOfInstallments"] = count_payment
    

    context = {
        'form_Accounts':form_Accounts,
        'service_form':service_form,
        'service_item_formset':service_item_formset,
        'form_payment_account':PaymentMethod_Accounts_FormSet,
        'venda_item_formset':venda_item_formset,
        'older_form_payment_account':Older_PaymentMethod_Accounts_FormSet,
        'permition_edit_sale':permit_edition_sale,
        'permition_edit_saleItem':permit_edition_saleItem,
        'permition_edit_saleServiceItem':permit_edition_saleService,
        'permition_edit_payments':permit_edition_payment
    }

    return render(request,'workOrdersUpdate.html',context) 

@login_required
def workOrder(request):
    situations = Situation.objects.filter(is_Active = True)
    options_situations = 1
    # options_situations = Situation.CLOSURE_LEVEL_OPTIONS
    context = {
        'workOrders':Vendaservice.objects.all(),
        'situations':situations,
        'options_situations':options_situations
    }

   
    return render(request,'workOrders_list.html',context)

@login_required
@transaction.atomic 
def workOrders_delete(request,pk):
        workOrders = get_object_or_404(Vendaservice, pk=pk)

        if request.method == "POST":
            pessoa = workOrders.pessoa
            value_payments = PaymentMethod_Accounts.objects.filter(ordem_servico=workOrders.id,activeCredit=True)
            for value_payment in value_payments:
                pessoa.creditLimit+=value_payment.value
            pessoa.save()
            workOrders.delete()
            messages.success(request, "Ordem de Serviço deletada com sucesso.",extra_tags="successWorkOrder")
            return redirect('workOrders_list')

        context ={
            'workOrders':workOrders
        }
        return render(request,'workOrders_list.html',context)

def service_search(request):
   
    query = request.GET.get('query', '') 
    resultados = Service.objects.filter(
        (
            Q(id__icontains=query) |
            Q(name_service__icontains=query)
        )
        & Q(is_Active =True)
    ).order_by('id')[:5]
    services = [
        {
            'id':servico.id,
            'name_service':servico.name_service,
            'price':servico.value_service
        }
        for servico in resultados
    ]

    return JsonResponse({'servicos':services})

def get_service_id(request):
    query = request.GET.get('query','')
    resultados = Service.objects.filter(
        Q(id=query)
    )
    resultados_json = list(resultados.values('id','name_service'))
    return JsonResponse({'servico':resultados_json})


def mudar_situacao_service(request,pk):
    nova_situacao = request.POST.get('opcao')
    situationObject = get_object_or_404(Situation,pk=nova_situacao)
    venda = get_object_or_404(Vendaservice,pk=pk)
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
                    categoria = "Serviço",
                    
                )
        
            # messages.success(request, 'Caixa Aberto Com Sucesso')
            venda.save() 
            return redirect('venda_list')
        else:
            messages.error(request,'Caixa com este usuário não está aberto!')
            return redirect('venda_list')
        
    return redirect('venda_list')