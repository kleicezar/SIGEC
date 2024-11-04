from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *

def index(request):
    return render(request, 'config/index.html')

### PAYMENT METHOD

def paymentMethod(request):
    context = {
        'PaymentMethods': PaymentMethod.objects.all()
    }
    return render(request, 'config/PaymentMethod.html', context)

def PaymentMethodForm(request):
    if request.method == "GET":
        paymentMethodForm = PaymentMethodModelForm()
        context = {
            'paymentMethod' : paymentMethodForm
        }
        return render(request, 'config/PaymentMethodForm.html', context)
    else:
        paymentMethodForm = PaymentMethodModelForm(request.POST)
        if paymentMethodForm.is_valid():
            paymentMethodForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('PaymentMethod')
    context = {
        'paymentMethod' : paymentMethodForm
    }
    return render(request, 'config/PaymentMethod.html', context)
    
def updatePaymentMethod(request, id_paymentMethod):
    paymentMethod = get_object_or_404(PaymentMethod, id=id_paymentMethod)
    if request.method == "GET":
        paymentMethodForm = PaymentMethodModelForm(instance=paymentMethod)

        context = {
            'PaymentMethod': paymentMethod,
            'paymentMethod': paymentMethodForm
        }
        return render(request, 'config/PaymentMethodForm.html',context)
    elif request.method == "POST":
        paymentMethodForm = PaymentMethodModelForm(request.POST, instance=paymentMethod)
        if paymentMethodForm.is_valid():
            paymentMethodForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('PaymentMethod')
    context = {
        'PaymentMethod' : paymentMethodForm
    }
    return render(request, 'config/PaymentMethod.html', context)

def deletePaymentMethod(request, id_paymentMethod):
    paymentMethod = get_object_or_404(PaymentMethod, id=id_paymentMethod)
    if request.method == "POST":
        paymentMethod.delete()
        messages.success(request, "Situação deletada com sucesso.")
        return redirect('PaymentMethod')  # Redirecione para onde desejar
    context = {
        'paymentMethod': paymentMethod
    }

    return render(request, 'config/PaymentMethod.html', context)

### POSITION

def position(request):
    context = {
        'Positions': Position.objects.all()
    }
    return render(request, 'config/Position.html', context)

def PositionForm(request):
    if request.method == "GET":
        PositionForm = PositionModelForm()
        context = {
            'Position' : PositionForm
        }
        return render(request, 'config/PositionForm.html', context)
    else:
        PositionForm = PositionModelForm(request.POST)
        if PositionForm.is_valid():
            PositionForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('Position')
    context = {
        'Position' : PositionForm
    }
    return render(request, 'config/Position.html', context)

def updatePosition(request, id_position):
    position = get_object_or_404(Position, id=id_position)
    if request.method == "GET":
        positionForm = PositionModelForm(instance=position)

        context = {
            'position': position,
            'Position': positionForm
        }
        return render(request, 'config/PositionForm.html',context)
    elif request.method == "POST":
        positionForm = PositionModelForm(request.POST, instance=position)
        if positionForm.is_valid():
            positionForm.save()
            messages.success(request, "Cargo cadastrado com sucesso")
            return redirect('Position')
    context = {
        'Position' : positionForm
    }
    return render(request, 'config/Position.html', context)

def deletePosition(request, id_position):
    position = get_object_or_404(Position, id=id_position)
    if request.method == "POST":
        position.delete()
        messages.success(request, "Situação deletada com sucesso.")
        return redirect('Position')  # Redirecione para onde desejar
    context = {
        'position': position
    }

    return render(request, 'config/Position.html', context)

### SITUATION

def situation(request):
    context = {
        'Situations': Situation.objects.all()
    }
    return render(request, 'config/Situation.html', context)

def SituationForm(request):
    if request.method == "GET":
        situationForm = SituationModelForm()
        context = {
            'Situation' : situationForm
        }
        return render(request, 'config/SituationForm.html', context)
    else:
        situationForm = SituationModelForm(request.POST)
        if situationForm.is_valid():
            situationForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('Situation')
    context = {
        'Situation' : situationForm
    }
    return render(request, 'config/Situation.html', context)

def updateSituation(request, id_situation):
    situation = get_object_or_404(Situation, id=id_situation)
    if request.method == "GET":
        situationForm = SituationModelForm(instance=situation)

        context = {
            'situation': situation,
            'Situation': situationForm
        }
        return render(request, 'config/SituationForm.html',context)
    elif request.method == "POST":
        situationForm = SituationModelForm(request.POST, instance=situation)
        if situationForm.is_valid():
            situationForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('Situation')
    context = {
        'Situation' : situationForm
    }
    return render(request, 'config/Situation.html', context)

def deleteSituation(request, id_situation):
    situation = get_object_or_404(Situation, id=id_situation)
    if request.method == "POST":
        situation.delete()
        messages.success(request, "Situação deletada com sucesso.")
        return redirect('Situation')  # Redirecione para onde desejar
    context = {
        'situation': situation
    }

    return render(request, 'config/Situation.html', context)



### SUPPLIER

# def supplier(request):
#     context = {
#         'Suppliers': Person.objects.all()
#     }
#     return render(request, 'config/supplier.html', context)

# def supplierForm(request):
#     if request.method == "GET":
#         supplierForm = SupplierModelForm()
#         context = {
#             'Supplier' : supplierForm
#         }
#         return render(request, 'config/SupplierForm.html', context)
#     else:
#         supplierForm = SupplierModelForm(request.POST)
#         if supplierForm.is_valid():
#             supplierForm.save()
#             messages.success(request, "Forma de Pagamento cadastrado com sucesso")
#             return redirect('Supplier')
#     context = {
#         'Supplier' : supplierForm
#     }
#     return render(request, 'config/Supplier.html', context)

# def updateSupplier(request, id_supplier):
#     supplier = get_object_or_404(Person, id=id_supplier)
#     if request.method == "GET":
#         supplierForm = SupplierModelForm(instance=supplier)

#         context = {
#             'Supplier': supplier,
#             'supplier': supplierForm
#         }
#         return render(request, 'config/SupplierForm.html',context)
#     elif request.method == "POST":
#         supplierForm = SupplierModelForm(request.POST, instance=supplier)
#         if supplierForm.is_valid():
#             supplierForm.save()
#             messages.success(request, "Forma de Pagamento cadastrado com sucesso")
#             return redirect('Supplier')
#     context = {
#         'Supplier' : supplierForm
#     }
#     return render(request, 'config/supplier.html', context)

# def deleteSupplier(request, id_supplier):
#     supplier = get_object_or_404(Person, id=id_supplier)
#     if request.method == "POST":
#         supplier.delete()
#         messages.success(request, "Situação deletada com sucesso.")
#         return redirect('Supplier') 
#     context = {
#         'Supplier': supplier
#     }

#     return render(request, 'config/Supplier.html', context)

def supplier(request):
    persons = Person.objects.all()
    return render(request, 'config/supplier.html', {'persons': persons})

# Criar uma nova pessoa
def supplierForm(request):
    if request.method == 'POST':
        form = SupplierModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Supplier')
    else:
        form = SupplierModelForm()
    return render(request, 'config/supplierForm.html', {'form': form})

# Atualizar uma pessoa existente
def updateSupplier(request, id_supplier):
    person = get_object_or_404(Person, id=id_supplier)
    if request.method == 'POST':
        form = SupplierModelForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('Supplier')
    else:
        form = SupplierModelForm(instance=person)
    return render(request, 'config/supplierForm.html', {'form': form})

# Deletar uma pessoa
def deleteSupplier(request, id_supplier):
    person = get_object_or_404(Person, id=id_supplier)
    if request.method == 'POST':
        person.delete()
        return redirect('Supplier')
    return render(request, 'config/person_confirm_delete.html', {'person': person})


### PRODUCT

def product(request):
    products = Product.objects.all()
    return render(request, 'config/product_list.html', {'products': products})

# Criar novo produto
def productForm(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Product')
    else:
        form = ProductModelForm()
    return render(request, 'config/product_form.html', {'form': form})

# Atualizar produto existente
def updateProduct(request, id_product):
    product = get_object_or_404(Product, id=id_product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('Product')
    else:
        form = ProductModelForm(instance=product)
    return render(request, 'config/product_form.html', {'form': form})

# Deletar produto
def deleteProduct(request, id_product):
    product = get_object_or_404(Product, id=id_product)
    if request.method == 'POST':
        product.delete()
        return redirect('Product')
    return render(request, 'config/product_confirm_delete.html', {'product': product})




### CLIENT

# def client(request):
#     context = {
#         'Client': Person.objects.all()
#     }
#     return render(request, 'config/client.html', context)

# def clientForm(request):
#     if request.method == "GET":
#         # address_form = AddressModelForm(request.POST)
#         client_form = PersonModelForm(request.POST)

#         context = {
#             # 'address_form' : address_form,
#             'client_form': client_form
#         }
#         return render(request, 'config/clientForm.html', context)
#     else:
#         if clientForm.is_valid():
#             clientForm.save()
#             messages.success(request, "Fornecedor cadastrado com sucesso")
#             return redirect('Supplier')
#     context = {
#         'legalPerson_form' : legalPerson_form,
#     }
#     return render(request, 'config/client.html', context)

