
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from finance.forms import AccountsForm, PaymentMethodAccountsForm,PaymentMethodFormSet
from finance.models import PaymentMethod_Accounts
from .forms import *
from .models import *
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db import transaction

@login_required
@transaction.atomic 
def workOrders_create(request):
    ServiceItemFormSet  = inlineformset_factory(VendaService,VendaItemService,form=VendaItemServiceForm,extra=1,can_delete=True)
    VendaItemFormSet = inlineformset_factory(VendaService, VendaItem, form=VendaItemForm, extra=1, can_delete=True)
    # PaymentMethodServiceFormSet = inlineformset_factory(VendaService,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=1,can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(VendaService,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=1,can_delete=True)
    
    if(request.method == 'POST'):
        service_form = VendaServiceForm(request.POST)
        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)
        service_item_formset = ServiceItemFormSet(request.POST)
        venda_item_formset = VendaItemFormSet(request.POST)

        if(service_form.is_valid() and venda_item_formset.is_valid() and service_item_formset.is_valid() and PaymentMethod_Accounts_FormSet.is_valid()):
            service = service_form.save(commit=False)

            venda_item_formset.instance = service
            venda_item_formset.save(commit=False)

            service_item_formset.instance = service
            service_item_formset.save(commit=False)

            PaymentMethod_Accounts_FormSet.instance = service
            total_payment = 0
            total_payment_with_credit = 0
            for form in PaymentMethod_Accounts_FormSet:
                # form.instance = service
                if form.cleaned_data:
                    form.acc = False
                    valor = form.cleaned_data['value']
                    total_payment+=valor
                    # valid_payments.append(form)

                    name_payment = form.cleaned_data["forma_pagamento"]
                    paymentWithCredit = PaymentMethod.objects.filter(
                        name_paymentMethod=name_payment,creditPermission=True
                    )
                    if paymentWithCredit.exists():
                        total_payment_with_credit+=valor
                        form.instance.activeCredit=True

            pessoa = service_form.cleaned_data["pessoa"]

            creditLimit = pessoa.creditLimit
            creditLimitAtual = creditLimit
            creditLimitAtual -= total_payment_with_credit

            if(total_payment==service.total_value + service.total_value_service) and ( (creditLimitAtual == creditLimit) or (creditLimitAtual != creditLimit and creditLimitAtual>=0) ):
                pessoa.creditLimit = creditLimitAtual
                pessoa.save()

                service_form.save()
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

            if ((creditLimitAtual != creditLimit) or (creditLimitAtual != creditLimit and creditLimitAtual<0)):
                messages.warning(request,"Ação Cancelada! O valor acumulado dos pagamentos é menor que o limite de crédito. ",extra_tags='workcreate_page')

        if not service_form.is_valid():
            print("Erro no ServiceForm",service_form.errors)

        if not venda_item_formset.is_valid():
            print("Erro na VendaItem",venda_item_formset.errors)
            
        if not service_item_formset.is_valid():
            print("Erro no VendaServiceItem",service_item_formset.errors)

        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no VendaPagamentoService",PaymentMethod_Accounts_FormSet.errors)

       
    else:
        form_Accounts = AccountsForm()
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        service_form = VendaServiceForm()
        service_item_formset = ServiceItemFormSet(queryset=VendaItemService.objects.none())
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

    servico = get_object_or_404(VendaService, pk=pk)
    ServiceItemFormSet  = inlineformset_factory(VendaService,VendaItemService,form=VendaItemServiceForm,extra=0,can_delete=True)
    VendaItemFormSet = inlineformset_factory(VendaService, VendaItem, form=VendaItemForm, extra=0, can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(VendaService,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=1,can_delete=True)
    Older_PaymentMethod_Accounts_FormSet = inlineformset_factory(VendaService, PaymentMethod_Accounts, form=PaymentMethodAccountsForm, extra=0, can_delete=True)

    if request.method == 'POST':
        previous_url = request.session.get('previous_page','/')
        # print(request.POST)
        service_form = VendaServiceForm(request.POST, instance=servico)
        service_item_formset = ServiceItemFormSet(request.POST, instance=servico)
        venda_item_formset = VendaItemFormSet(request.POST,instance=servico,prefix='vendaitemproductservice_set')
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST, instance=servico,prefix="paymentmethod_accounts_set")
        Older_PaymentMethod_Accounts_FormSet = Older_PaymentMethod_Accounts_FormSet(request.POST,instance=servico,prefix="older_paymentmethod_accounts_set")

        venda_item = VendaItem.objects.filter(venda=servico)
        ids_existentes_venda_itens = set(venda_item.values_list('id',flat=True))
        ids_enviados_venda_itens = set(
            int(value) for key, value in request.POST.items() 
            if key.startswith("vendaitemproductservice_set-") and key.endswith("-id") and value.isdigit()
            )
        ids_para_excluir_venda_itens = ids_existentes_venda_itens - ids_enviados_venda_itens
        VendaItem.objects.filter(id__in=ids_para_excluir_venda_itens).delete()
        

        venda_service_item = VendaItemService.objects.filter(venda=servico)
        ids_existentes_venda_service_itens = set(venda_service_item.values_list('id',flat=True))
        ids_enviados_vendas_service_itens = set(
             int(value) for key, value in request.POST.items() 
            if key.startswith("vendaitemservice_set-") and key.endswith("-id") and value.isdigit()
        )
        ids_para_excluir_venda_service_itens = ids_existentes_venda_service_itens - ids_enviados_vendas_service_itens
        VendaItemService.objects.filter(id__in=ids_para_excluir_venda_service_itens).delete()


        if(service_form.is_valid() and venda_item_formset.is_valid() and service_item_formset.is_valid() and PaymentMethod_Accounts_FormSet.is_valid()) and Older_PaymentMethod_Accounts_FormSet.is_valid() :
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
            
            # payments_instances = PaymentMethod_Accounts_FormSet.save(commit=False)
            # pagamentos_paga_deletar = []

            # for form in PaymentMethod_Accounts_FormSet.deleted_forms:
            #     if form.instance.pk is not None:
            #         pagamentos_paga_deletar.append(form.instance)

            pessoa = service_form.cleaned_data["pessoa"]
            value_payments = PaymentMethod_Accounts.objects.filter(ordem_servico = servico.id,activeCredit = True)

            for value_payment in value_payments:
                pessoa.creditLimit += value_payment.value
            pessoa.save()

            total_payment = 0
            total_payment_with_credit = 0

            onlyOldPayments = False 
            try:
                for form in PaymentMethod_Accounts_FormSet:
                    name_payment = form.cleaned_data["forma_pagamento"]
                    paymentWithCredit = PaymentMethod.objects.filter(
                        name_paymentMethod = name_payment,creditPermission=True
                    )
                    if form.cleaned_data:
                        valor = form.cleaned_data['value']
                        if not form.cleaned_data['DELETE']:
                            if paymentWithCredit.exists():
                                total_payment_with_credit+= form.cleaned_data["value"]
                            total_payment+=valor
            except TypeError:
                onlyOldPayments = True
                for form in Older_PaymentMethod_Accounts_FormSet:
                    name_payment = form.cleaned_data["forma_pagamento"]
                    paymentWithCredit = PaymentMethod.objects.filter(
                        name_paymentMethod = name_payment,creditPermission=True
                    )
                    
                    if form.cleaned_data:
                        valor = form.cleaned_data['value']
                        if not form.cleaned_data["DELETE"] :
                            if paymentWithCredit.exists():
                                total_payment_with_credit +=form.cleaned_data["value"]
                            total_payment += valor

            creditLimit = pessoa.creditLimit
            creditLimitAtual = creditLimit
            creditLimitAtual-= total_payment_with_credit

            if (total_payment == service.total_value + service.total_value_service) and ( (creditLimitAtual == creditLimit) or (creditLimitAtual != creditLimit and creditLimitAtual >= 0)):
                pessoa.creditLimit = creditLimitAtual
                pessoa.save()

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
                else:
                    Older_PaymentMethod_Accounts_FormSet.save()
            
                messages.success(request,"Ordem de Serviço atualizada com sucesso.",extra_tags="successWorkOrder")
                return redirect(previous_url)
            
            if total_payment != service.total_value:
                messages.warning(request,"Ação cancelada! O valor acumalado dos pagamentos é menor do que o valor acumulado dos prudutos.",extra_tags='workupdate_page')
            
            if ((creditLimitAtual != creditLimit) or (creditLimitAtual != creditLimit and creditLimitAtual<0)):
                messages.warning(request,"Ação Cancelada! O valor acumulado dos pagamentos é menor que o limite de crédito. ",extra_tags='workupdate_page')

        if not service_form.is_valid():
            print("Erro no ServiceForm",service_form.errors)

        if not venda_item_formset.is_valid():
            print("Erro no VendaItem",venda_item_formset.errors)

        if not service_item_formset.is_valid():
            print("Erro no VendaServiceItem",service_item_formset.errors)
            
        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no VendaPagamentoService",PaymentMethod_Accounts_FormSet.errors)
        
        if not Older_PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no Older_PaymentMethod_Accounts_FormSet",Older_PaymentMethod_Accounts_FormSet.errors)
        
      
      
    else:
        form_Accounts = AccountsForm(instance=servico)
        older_payment_method_formset = Older_PaymentMethod_Accounts_FormSet(queryset=servico.paymentmethod_accounts_set.all(),instance=servico,prefix='older_paymentmethod_accounts_set')
        payment_method_formset = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        service_form = VendaServiceForm(instance=servico)
        venda_item_formset = VendaItemFormSet(queryset=servico.vendaitem_set.all(),instance=servico,prefix='vendaitemproductservice_set')
        service_item_formset = ServiceItemFormSet(queryset = servico.vendaitemservice_set.all(),instance=servico)
       
        count_payment = 0
       
        for i,form in enumerate(older_payment_method_formset):
            if i == 0:
                data_obj = form.initial["expirationDate"]  
                data_modificada = data_obj - timedelta(days=int(form.initial["days"])) 
                data_modificada = datetime.strptime(str(data_modificada), "%Y-%m-%d").strftime("%d/%m/%Y") 

            count_payment+=1
        form_Accounts.initial["date_init"] = data_modificada
        form_Accounts.initial["totalValue"] = service_form.initial['total_value'] + service_form.initial['total_value_service']
        form_Accounts.initial["numberOfInstallments"] = count_payment
        
        if 'HTTP_REFERER' in request.META:
            request.session['previous_page'] = request.META['HTTP_REFERER']
    context = {
            'form_Accounts':form_Accounts,
            'service_form':service_form,
            'service_item_formset':service_item_formset,
            'form_payment_account':payment_method_formset,
            'venda_item_formset':venda_item_formset,
            'older_form_payment_account':older_payment_method_formset
            # 'form_payment_account':payment_method_formset
        }

    return render(request,'workOrdersUpdate.html',context) 

@login_required
def workOrder(request):
    context = {
        'workOrders':VendaService.objects.all()
    }
    return render(request,'workOrders_list.html',context)

@login_required
@transaction.atomic 
def workOrders_delete(request,pk):
        workOrders = get_object_or_404(VendaService, pk=pk)

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
    resultados = service.objects.filter(
        (
            Q(id__icontains=query) |
            Q(name_Service__icontains=query)
        )
        & Q(is_Active =True)
    ).order_by('id')[:5]
    services = [
        {
            'id':servico.id,
            'name_Service':servico.name_Service,
            'price':servico.value_Service
        }
        for servico in resultados
    ]

    return JsonResponse({'servicos':services})

def get_service_id(request):
    query = request.GET.get('query','')
    resultados = service.objects.filter(
        Q(id=query)
    )
    resultados_json = list(resultados.values('id','name_Service'))
    return JsonResponse({'servico':resultados_json})