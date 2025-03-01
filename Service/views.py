
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
    ServiceItemFormSet  = inlineformset_factory(VendaService,VendaItemService,form=VendaItemForm,extra=1,can_delete=True)
    PaymentMethodServiceFormSet = inlineformset_factory(VendaService,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=1,can_delete=True)
    PaymentMethodAccountsFormSet = inlineformset_factory(VendaService,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=1,can_delete=True)

    if(request.method == 'POST'):
        service_form = VendaServiceForm(request.POST)
        form_Accounts = AccountsForm(request.POST)
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(request.POST)
        service_item_formset = ServiceItemFormSet(request.POST)
        payment_method_formset = PaymentMethodServiceFormSet(request.POST)

        if(service_form.is_valid() and service_item_formset.is_valid() and payment_method_formset.is_valid()):
            print('formulários válidos')
            service = service_form.save()
            service_item_formset.instance = service
            service_item_formset.save()

            payment_method_formset.instance = service
            total_payment = 0
            payments_to_delete = []
            valid_payments = []
            for form in payment_method_formset:
                # form.instance = service
                if form.cleaned_data:
                    form.acc = True
                    if form.cleaned_data.get("DELETE",False):
                        payments_to_delete.append(form.instance)
                    else:
                        valor = form.cleaned_data['value']
                        total_payment+=valor
                        valid_payments.append(form)

            if(total_payment==service.total_value):
                for form in valid_payments:
                    form.instance.ordem_servico = service
                    form.save()
                    print('✅ Pagamentos foram salvos!')

                    # 🔍 Tente recarregar um objeto do banco para testar
                for payment in payments_to_delete:
                    payment.delete()

                # for form in payment_method_formset.deleted_objects:
                #     form.delete()
                #     form.save(
        elif not service_form.is_valid():
            print("Erro  no ServiceForm",service_form.errors)

        elif not service_item_formset.is_valid():
            print("Erro no VendaServiceItem",service_item_formset.errors)

        elif not payment_method_formset.is_valid():
            print("Erro no VendaPagamentoService",payment_method_formset.errors)

        return  redirect('serviceForm')
    
    else:
        form_Accounts = AccountsForm()
        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())
        service_form = VendaServiceForm()
        service_item_formset = ServiceItemFormSet(queryset=VendaItemService.objects.none())
        payment_method_formset = PaymentMethodServiceFormSet(queryset=PaymentMethod_VendaService.objects.none())

        context = {
            'form_Accounts':form_Accounts,
            'form_payment_account':PaymentMethod_Accounts_FormSet,
            'service_form':service_form,
            'service_item_formset':service_item_formset,
            'payment_method_formset':payment_method_formset
        }

        return render(request,'serviceOrder_form.html',context)

def workerService_update(request,pk):

    servico = get_object_or_404(VendaService, pk=pk)
    ServiceItemFormSet  = inlineformset_factory(VendaService,VendaItemService,form=VendaItemForm,extra=0,can_delete=True)
    PaymentMethodServiceFormSet = inlineformset_factory(VendaService,PaymentMethod_Accounts,form=PaymentMethodAccountsForm,extra=0,can_delete=True)

    if request.method == 'POST':

        service_form = VendaServiceForm(request.POST)
        service_item_formset = ServiceItemFormSet(request.POST)
        payment_method_formset = PaymentMethodServiceFormSet(request.POST)
        if(service_form.is_valid() and service_item_formset.is_valid() and payment_method_formset.is_valid()):
            ...

            service_form.save()

            service_item_instances = service_item_formset.save(commit=False)
            service_item_formset.save_m2m()

            itens_para_deletar = []
            
            for form in service_item_formset.deleted_forms:
                if form.instance.pk is not None:
                    itens_para_deletar.append(form.instance)

            for instance in service_item_instances:
                instance.save()

            for item in itens_para_deletar:
                item.delete()

            payments_instances = service_item_formset.save(commit=False)
            pagamentos_paga_deletar = []

            for form in payment_method_formset.deleted_forms:
                if form.instance.pk is not None:
                    pagamentos_paga_deletar.append(form.instance)

            for instance in payments_instances:
                instance.save()

            for pagamento in pagamentos_paga_deletar:
                pagamento.delete()
            payment_method_formset.save()

            messages.success(request,"Venda de Servico atualizada com sucesso!")
            return redirect('OrderService')
            # print('formulários válidos')
            # venda = service_form.save()
            # for form in service_item_formset:
            #     if form.cleaned_data:
            #         servico = form.cleaned_data['service']
            #         preco = form.cleaned_data['preco']
            #         discount = form.cleaned_data['discount']
            #         if not form.cleaned_data.get("DELETE"):
            #             VendaItemService.objects.create(
            #                 venda = venda,
            #                 service = servico,
            #                 preco = preco,
            #                 discount = discount
            #             )
            #             service_item_formset.instance = venda

            # payment_method_formset.instance = venda
            # total_payment = 0
            # for form in payment_method_formset:
            #     if form.cleaned_data:
            #         valor = form.cleaned_data['valor']
            #         total_payment+=valor
            # if(total_payment==service_form.cleaned_data['total_value']):
            #     payment_method_formset.save()
            #     for form in payment_method_formset.deleted_objects:
            #         form.delete()
            #         form.save()

        elif not service_form.is_valid():
            print("Erro  no ServiceForm",service_form.errors)
        elif not service_item_formset.is_valid():
            print("Erro no VendaServiceItem",service_item_formset.errors)
        elif not payment_method_formset.is_valid():
            print("Erro no VendaPagamentoService",payment_method_formset.errors)
        return  redirect('serviceForm')
    
    else:
        form_Accounts = AccountsForm(instance=servico)
        service_form = VendaServiceForm(instance=servico)
        service_item_formset = ServiceItemFormSet(instance=servico)
        payment_method_formset = PaymentMethodServiceFormSet(instance=servico)

        context = {
            'form_Accounts':form_Accounts,
            'service_form':service_form,
            'service_item_formset':service_item_formset,
            'form_payment_account':payment_method_formset
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
            workService.delete()
            messages.success(request, "Serviço deletada com sucesso.")
            return redirect('OrderService')
        print('opa')
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