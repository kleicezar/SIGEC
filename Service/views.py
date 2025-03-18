
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from finance.forms import AccountsForm, PaymentMethodAccountsForm
from finance.models import PaymentMethod_Accounts
from .forms import *
from .models import *
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse

@login_required
def service(request):
    context = {
        'Services':Service.objects.all()
    }
    return render(request,'service_list.html',context)
    # return HttpResponse("Olá, esta é a minha nova app Django!")

def service_create(request):
    if request.method == 'POST':
        service_form = ServiceForm(request.POST)
        print(f'\n\n\n{request.POST}')
        print(f'\n\n\n{service_form.is_valid()}')
        if service_form.is_valid():
            service_form.save() 
            messages.success(request, "Tipo de Serviço cadastrado com sucesso")
            return redirect('service_list')
        else: 
            return render(request, 'service_form.html', {'form': service_form})
    else:
        service_form = ServiceForm()
        context = {
            'service':service_form
        }
        return render(request,'service_form.html',context)
    
       
def service_update(request,pk):
    servico = get_object_or_404(Service,pk=pk)
    if request.method == "POST":
        service_form = ServiceForm(request.POST,instance=servico)
        if service_form.is_valid():
            service_form.save()
            messages.success(request, "Tipo de Serviço atualizado com sucesso")
            return redirect('orderServiceForm')

        print(service_form.errors)
    else:
        service_form = ServiceForm(instance=servico)
        context = {
            'service':service_form,
        }
        return render(request,'service_form.html',context)

def delete_service(request,pk):
    servico = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        servico.delete()
        messages.success(request, "Serviço deletada com sucesso.")
        return redirect('service_list')
    context ={
        'service':servico
    }
    return render(request,'service_list',context)

def workerService_create(request):
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
        # payment_method_formset = PaymentMethodServiceFormSet(request.POST)

        if(service_form.is_valid() and venda_item_formset.is_valid() and service_item_formset.is_valid() and PaymentMethod_Accounts_FormSet.is_valid()):
            service = service_form.save(commit=False)

            venda_item_formset.instance = service
            venda_item_formset.save(commit=False)

            service_item_formset.instance = service
            service_item_formset.save(commit=False)

            PaymentMethod_Accounts_FormSet.instance = service
            total_payment = 0
            payments_to_delete = []
            valid_payments = []
            total_payment_with_credit = 0
            for form in PaymentMethod_Accounts_FormSet:
                # form.instance = service
                if form.cleaned_data:
                    form.acc = False
                    if form.cleaned_data.get("DELETE",False):
                        payments_to_delete.append(form.instance)
                    else:
                        valor = form.cleaned_data['value']
                        total_payment+=valor
                        valid_payments.append(form)

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

                for form in valid_payments:
                    form.instance.ordem_servico = service
                    form.save()

                for payment in payments_to_delete:
                    payment.delete()

                # for form in PaymentMethod_Accounts_FormSet.deleted_objects:
                #     form.delete()
                #     form.save(
        if not service_form.is_valid():
            print("Erro  no ServiceForm",service_form.errors)

        if not venda_item_formset.is_valid():
            print("Erro na VendaItem",venda_item_formset.errors)
            
        if not service_item_formset.is_valid():
            print("Erro no VendaServiceItem",service_item_formset.errors)

        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no VendaPagamentoService",PaymentMethod_Accounts_FormSet.errors)

        return  redirect('OrderService')
    
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

        return render(request,'serviceOrder_form.html',context)

def workerService_update(request,pk):

    servico = get_object_or_404(VendaService, pk=pk)
    ServiceItemFormSet  = inlineformset_factory(VendaService,VendaItemService,form=VendaItemServiceForm,extra=0,can_delete=True)
    VendaItemFormSet = inlineformset_factory(VendaService, VendaItem, form=VendaItemForm, extra=0, can_delete=True)

    PaymentMethodAccountsFormSet = inlineformset_factory(VendaService,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=1,can_delete=True)

    if request.method == 'POST':
        
        service_form = VendaServiceForm(request.POST, instance=servico)
        service_item_formset = ServiceItemFormSet(request.POST, instance=servico)
        venda_item_formset = VendaItemFormSet(request.POST,instance=servico)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST, instance=servico)

        venda_item = VendaItem.objects.filter(venda=servico)
        ids_existentes_venda_itens = set(venda_item.values_list('id',flat=True))
        ids_enviados_venda_itens = set(
            int(value) for key, value in request.POST.items() 
            if key.startswith("vendaitem_set-") and key.endswith("-id") and value.isdigit()
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


        if(service_form.is_valid() and venda_item_formset.is_valid() and service_item_formset.is_valid() and PaymentMethod_Accounts_FormSet.is_valid()):
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
            
            payments_instances = PaymentMethod_Accounts_FormSet.save(commit=False)
            pagamentos_paga_deletar = []

            for form in PaymentMethod_Accounts_FormSet.deleted_forms:
                if form.instance.pk is not None:
                    pagamentos_paga_deletar.append(form.instance)

            pessoa = service_form.cleaned_data["pessoa"]
            value_payments = PaymentMethod_Accounts.objects.filter(ordem_servico = servico.id,activeCredit = True)

            for value_payment in value_payments:
                pessoa.creditLimit += value_payment.value
            pessoa.save()

            total_payment = 0
            total_payment_with_credit = 0

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

                for instance in payments_instances:
                    instance.save()
                
                for pagamento in pagamentos_paga_deletar:
                    pagamento.delete()

                return redirect('OrderService')
    
        if not service_form.is_valid():
            print("Erro no ServiceForm",service_form.errors)

        if not venda_item_formset.is_valid():
            print("Erro no VendaItem",venda_item_formset.errors)

        if not service_item_formset.is_valid():
            print("Erro no VendaServiceItem",service_item_formset.errors)
            
        if not PaymentMethod_Accounts_FormSet.is_valid():
            print("Erro no VendaPagamentoService",PaymentMethod_Accounts_FormSet.errors)
        
        return redirect('OrderService')
    else:
        form_Accounts = AccountsForm(instance=servico)
        service_form = VendaServiceForm(instance=servico)
        service_item_formset = ServiceItemFormSet(queryset = servico.vendaitemservice_set.all(),instance=servico)
        payment_method_formset = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        venda_item_formset = VendaItemFormSet(queryset=servico.vendaitem_set.all(),instance=servico)
        older_payment_method_formset =  PaymentMethodAccountsFormSet(queryset=servico.paymentmethod_accounts_set.all(),instance=servico)
        count_payment = 0
       
        for i,form in enumerate(older_payment_method_formset):
            if i == 0:
                ...
                data_obj = form.initial["expirationDate"]  
                data_modificada = data_obj - timedelta(days=int(form.initial["days"])) 
                data_modificada = datetime.strptime(str(data_modificada), "%Y-%m-%d").strftime("%d/%m/%Y") 

            count_payment+=1
        form_Accounts.initial["date_init"] = data_modificada
        form_Accounts.initial["totalValue"] = service_form.initial['total_value'] + service_form.initial['total_value_service']
        form_Accounts.initial["numberOfInstallments"] = count_payment - 1

    context = {
            'form_Accounts':form_Accounts,
            'service_form':service_form,
            'service_item_formset':service_item_formset,
            'form_payment_account':payment_method_formset,
            'venda_item_formset':venda_item_formset,
            'older_form_payment_account':older_payment_method_formset
            # 'form_payment_account':payment_method_formset
        }

    return render(request,'serviceOrderUpdate.html',context) 

def workService(request):
    context = {
        
        'workServices':VendaService.objects.all()
    }
    return render(request,'serviceOrder.html',context)

def deleteWorkService(request,pk):
        workService = get_object_or_404(VendaService, pk=pk)

        if request.method == "POST":
            pessoa = workService.pessoa
            value_payments = PaymentMethod_Accounts.objects.filter(ordem_servico=workService.id,activeCredit=True)
            for value_payment in value_payments:
                pessoa.creditLimit+=value_payment.value
            pessoa.save()
            workService.delete()
            messages.success(request, "Serviço deletada com sucesso.")
            return redirect('OrderService')

        context ={
            'workService':workService
        }
        return render(request,'OrderService',context)
def service_search(request):
   
    query = request.GET.get('query', '') 
    print(query)
    resultados = Service.objects.filter(
        Q(id__icontains=query) |
       Q(name_Service__icontains=query)
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
    resultados = Service.objects.filter(
        Q(id=query)
    )
    resultados_json = list(resultados.values('id','name_Service'))
    return JsonResponse({'servico':resultados_json})