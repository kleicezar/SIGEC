from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse

def index(request):
    return HttpResponse("Olá, esta é a minha nova app Django!")


def service_create(request):
    if(request.method == 'GET'):
         service_form = ServiceForm()
         context = {
             'service':service_form
         }
         return render(request,'service_form.html',context)
    else:
       service_form = ServiceForm(request.POST)
       if service_form.is_valid():
            service_form.save()
            messages.success(request, "Tipo de Serviço cadastrado com sucesso")
            return redirect('orderServiceForm')
       

def workerService_create(request):
    ServiceItemFormSet  = inlineformset_factory(VendaService,VendaItemService,form=VendaItemForm,extra=1,can_delete=True)
    PaymentMethodServiceFormSet = inlineformset_factory(VendaService,PaymentMethod_VendaService,form=PaymentMethodVendaForm,extra=1,can_delete=True)

    if(request.method == 'POST'):
        service_form = VendaServiceForm(request.POST)
        service_item_formset = ServiceItemFormSet(request.POST)

        payment_method_formset = PaymentMethodServiceFormSet(request.POST)
        if(service_form.is_valid() and service_item_formset.is_valid() and payment_method_formset.is_valid()):
            print('formulários válidos')
            venda = service_form.save()
            for form in service_item_formset:
                if form.cleaned_data:
                    servico = form.cleaned_data['service']
                    preco = form.cleaned_data['preco']
                    discount = form.cleaned_data['discount']
                    if not form.cleaned_data.get("DELETE"):
                        VendaItemService.objects.create(
                            venda = venda,
                            service = servico,
                            preco = preco,
                            discount = discount
                        )
                    payment_method_formset.instance = venda
                    total_payment = 0
                    for form in payment_method_formset:
                        if form.cleaned_data:
                            valor = form.cleaned_data['valor']
                            total_payment+=valor
                    if(total_payment==service_form.cleaned_data['total_value']):
                        payment_method_formset.save()
                        for form in payment_method_formset.deleted_objects:
                            form.delete()
                            form.save()

        elif not service_form.is_valid():
            print("Erro  no ServiceForm",service_form.errors)
        elif not service_item_formset.is_valid():
            print("Erro no VendaServiceItem",service_item_formset.errors)
        elif not payment_method_formset.is_valid():
            print("Erro no VendaPagamentoService",payment_method_formset.errors)
        return  redirect('serviceForm')
    else:
        service_form = VendaServiceForm()
        service_item_formset = ServiceItemFormSet(queryset=VendaItemService.objects.none())
        payment_method_formset = PaymentMethodServiceFormSet(queryset=PaymentMethod_VendaService.objects.none())

        context = {
            'service_form':service_form,
            'service_item_formset':service_item_formset,
            'payment_method_formset':payment_method_formset
        }

        return render(request,'serviceOrder_form.html',context)
    
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
    