from django import forms
from .models import *

class AccountsPayableForm(forms.ModelForm):
    installment_Range = forms.ChoiceField(
        choices=AccountsPayable.INSTALLMENT_RANGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control row','id': 'installment_Range'}),
        label="Intervalo de Parcelas"
    )
    class Meta:
        model = AccountsPayable
        fields = [
            'pessoa_id', 
            'chartOfAccounts', 
            'documentNumber', 
            'date_account', 
            'numberOfInstallments',
            'installment_Range',
            'valueOfInstallments',
            'totalValue',
            'peopleWatching',
            'systemWatching',
            'date_init',
        ]
        widgets = { 
            'pessoa_id': forms.Select(attrs={ 
                'class': 'form-select row'
            }),
            'chartOfAccounts': forms.TextInput(attrs={
                'class': 'form-control row'
            }),
            'documentNumber': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'date_account': forms.TextInput(attrs={
                'class': 'form-control row mask-date'
            }),
            'numberOfInstallments': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            # 'installment_Range': forms.NumberInput(attrs={
            #     'class': 'form-control row',
            #     'min': 0
            # }),
            'valueOfInstallments': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'totalValue': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'peopleWatching': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'systemWatching': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'date_init': forms.TextInput(attrs={
                'class': 'form-control row mask-date'
            }),
        }


 
class PaymentMethod_AccountsPayableModelForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod_AccountsPayable
        fields = "__all__"
    
class PaymentMethodAccountsPayableForm(forms.ModelForm):
    # Definindo os campos manualmente
    interestType = forms.ChoiceField(
        choices=PaymentMethod_AccountsPayable.INTEREST_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control row','id': 'interest_type'}),
        label="Tipo de Juros"
    )
    fineType = forms.ChoiceField(
        choices=PaymentMethod_AccountsPayable.FINE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control row','id': 'fine_type'}),
        label="Tipo de Multa"
    )

    class Meta:
        model = PaymentMethod_AccountsPayable
        fields = [
            'forma_pagamento', 
            'expirationDate', 
            'days', 
            'value', 
            'interestPercent',
            'interestValue',
            'finePercent',
            'fineValue',
            'interestType',
            'fineType',
        ]
        widgets = { 
            'forma_pagamento': forms.Select(attrs={ 
                'class': 'form-select row'
            }),
            'expirationDate': forms.TextInput(attrs={
                'class': 'form-control row mask-date'
            }),
            'days': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'value': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'interestPercent': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'interestValue': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'finePercent': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'fineValue': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
        }

class AccountsReceivableModelForm(forms.ModelForm):
    class Meta:
        model = AccountsReceivable
        fields = "__all__"
       


class PaymentMethod_AccountsReceivableForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod_AccountsReceivable
        fields = "__all__"
        
# class PersonForm(forms.ModelForm):
#     class Meta:
#         model = Person
#         fields = ['WorkPhone', 
#                   'PersonalPhone', 
#                   'site', 'salesman', 
#                   'creditLimit', 
#                   'isClient', 
#                   'isSupllier', 
#                   'isUser', 
#                   'isEmployee', 
#                   'isSalesman', 
#                   'isFormer_employee', 
#                   'isCarrier', 
#                   'isDelivery_man', 
#                   'isTechnician'] # 'isActive'

        
# class ClientSearchForm(forms.Form): 
#     search = forms.CharField(max_length=100, required=False, label="Pesquisar Cliente")
