from django import forms
from .models import *

class AccountsForm(forms.ModelForm):
    installment_Range = forms.ChoiceField(
        choices=Accounts.INSTALLMENT_RANGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control row','id': 'installment_Range'}),
        label="Intervalo de Parcelas"
    )

    class Meta:
        model = Accounts
        fields = [ 
            'pessoa_id', 
            'chartOfAccounts', 
            'documentNumber', 
            'date_account', 
            'numberOfInstallments',
            'installment_Range',
            'totalValue',
            'peopleWatching',
            'systemWatching',
            'date_init',
        ]
        widgets = {
            'pessoa_id': forms.Select(attrs={ 
                'class': 'form-select row'
            }),
            'chartOfAccounts': forms.Select(attrs={
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
            'totalValue': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'peopleWatching': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'systemWatching': forms.TextInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'date_init': forms.TextInput(attrs={
                'class': 'form-control row mask-date'
            }),
        }

class PaymentMethodAccountsForm(forms.ModelForm):
    # Definindo os campos manualmente
    interestType = forms.ChoiceField(
        choices=PaymentMethod_Accounts.INTEREST_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control row','id': 'interest_type'}),
        label="Tipo de Juros"
    )
    fineType = forms.ChoiceField(
        choices=PaymentMethod_Accounts.FINE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control row','id': 'fine_type'}),
        label="Tipo de Multa"
    )

    class Meta:
        model = PaymentMethod_Accounts
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
            'expirationDate': forms.DateInput(format='%d/%m/%Y', attrs={
                'class': 'form-control row mask-date', 
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['interestType'].required = False
        self.fields['fineType'].required = False

class AccountsModelForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = "__all__"


