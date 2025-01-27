from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *

### PAYMENT METHOD
@login_required
def paymentMethod(request):
    context = {
        'PaymentMethods': PaymentMethod.objects.all()
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required
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

@login_required    
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

@login_required
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
@login_required
def position(request):
    context = {
        'Positions': Position.objects.all()
    }
    return render(request, 'config/Position.html', context)


@login_required
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

@login_required
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

@login_required
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

@login_required
def situation(request):
    context = {
        'Situations': Situation.objects.all()
    }
    return render(request, 'config/Situation.html', context)

@login_required
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

@login_required
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

@login_required
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

### ChartOfAccounts

@login_required
def chartOfAccounts(request):
    context = {
        'ChartOfAccountss': ChartOfAccounts.objects.all()
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
def ChartOfAccountsForm(request):
    if request.method == "GET":
        chartOfAccountsForm = ChartOfAccountsModelForm()
        context = {
            'ChartOfAccounts' : chartOfAccountsForm
        }
        return render(request, 'config/ChartOfAccountsForm.html', context)
    else:
        chartOfAccountsForm = ChartOfAccountsModelForm(request.POST)
        if chartOfAccountsForm.is_valid():
            chartOfAccountsForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('ChartOfAccounts')
    context = {
        'ChartOfAccounts' : chartOfAccountsForm
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
def updateChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "GET":
        chartOfAccountsForm = ChartOfAccountsModelForm(instance=chartOfAccounts)

        context = {
            'chartOfAccounts': chartOfAccounts,
            'ChartOfAccounts': chartOfAccountsForm
        }
        return render(request, 'config/ChartOfAccountsForm.html',context)
    elif request.method == "POST":
        chartOfAccountsForm = ChartOfAccountsModelForm(request.POST, instance=chartOfAccounts)
        if chartOfAccountsForm.is_valid():
            chartOfAccountsForm.save()
            messages.success(request, "Forma de Pagamento cadastrado com sucesso")
            return redirect('ChartOfAccounts')
    context = {
        'ChartOfAccounts' : chartOfAccountsForm
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
def deleteChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "POST":
        chartOfAccounts.delete()
        messages.success(request, "Situação deletada com sucesso.")
        return redirect('ChartOfAccounts')  # Redirecione para onde desejar
    context = {
        'chartOfAccounts': chartOfAccounts
    }

    return render(request, 'config/ChartOfAccounts.html', context)
