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
       

def orderService_create(request):
    VendaItemFormSet  = inlineformset_factory(VendaService,VendaItemService,form=VendaItemForm,extra=1,can_delete=True)
    PaymentMethodVendaFormSet = inlineformset_factory(VendaService,PaymentMethod_VendaService,form=PaymentMethodVendaForm,extra=1,can_delete=True)

    if(request.method == 'POST'):
        venda_form = VendaServiceForm(request.POST)
        ...
    else:
        venda_form = VendaServiceForm()
        venda_item_formset = VendaItemFormSet(queryset=VendaItemService.objects.none())
        payment_method_formset = PaymentMethodVendaFormSet(queryset=PaymentMethod_VendaService.objects.none())

        context = {
            'venda_form':venda_form,
            'venda_item_formset':venda_item_formset,
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
    