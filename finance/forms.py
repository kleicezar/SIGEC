from django import forms
from .models import *
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
class BaseAccountsForm(forms.ModelForm):
    """"
    Interface para formulários de contas. Define os campos usados.
    """

    class Meta:
        model = Accounts
        fields = [ 
            'pessoa_id', 
            'chartOfAccounts', 
            'documentNumber', 
            'date_account', 
            'peopleWatching',
            'systemWatching',
            
        ]
        widgets = {
            'documentNumber': forms.NumberInput(attrs={
                'class': 'form-control ',
                'min': 0
            }),
            'date_account': forms.TextInput(attrs={
                'class': 'form-control mask-date'
            }),
            'peopleWatching': forms.NumberInput(attrs={
                'class': 'form-control ',
                'min': 0
            }),
            'systemWatching': forms.TextInput(attrs={
                'class': 'form-control ',
                'min': 0
            }),
            
        }
    chartOfAccounts = forms.ModelChoiceField(
        queryset=ChartOfAccounts.objects.filter(is_Active=True),
        widget=forms.Select(
            attrs={
                'class':'form-control row'
            }
        ),
        label = 'Plano de Contas'
    )
    pessoa_id = forms.ModelChoiceField(
        queryset=Person.objects.filter(isActive=True),
        widget=forms.Select(
            attrs={
                'class':'form-control row'
            }
        )
    )

class AccountsForm(BaseAccountsForm):
    installment_Range = forms.ChoiceField(
        choices=Accounts.INSTALLMENT_RANGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control row'}),
        label="Intervalo de Parcelas"
    )


    class Meta(BaseAccountsForm.Meta):
        fields = [
            'pessoa_id', 
            'chartOfAccounts', 
            'documentNumber', 
            'date_account', 
            'peopleWatching',
            'systemWatching',
            'numberOfInstallments',
            'installment_Range',
            'totalValue',
            'date_init',
            'plannedAccount',
            'description'
        ]
        labels = {
            'chartOfAccounts':'Plano de Contas'
        }
        widgets={
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
                'class': 'form-control mt-2  mask-date'
            }),
            'numberOfInstallments': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'installment_Range': forms.Select(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'totalValue': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'date_init': forms.TextInput(attrs={
                'class': 'form-control row mask-date'
            }),
            'plannedAccounts':forms.CheckboxInput(attrs={'class':"form-check-input"}),
            'description':forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows': 3,
                    'cols': 40
                }
            )
            
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numberOfInstallments'].required = True 
        self.fields['installment_Range'].required = True 
        self.fields['totalValue'].required = True 
        self.fields['date_init'].required = True
        
class AccountsFormPlannedAccount(AccountsForm):
    installment_Range = forms.ChoiceField(
        choices=Accounts.INSTALLMENT_RANGE_CHOICES_PLANNED_ACCOUNT,
        widget=forms.Select(attrs={'class': 'form-control row'}),
        label="Intervalo de Parcelas"
    )

class AccountsFormUpdate(BaseAccountsForm):
    
    class Meta(BaseAccountsForm.Meta):
        exclude = ['numberOfInstallments','installment_Range','totalValue','date_init']
    
class BasePaymentMethodAccountsForm(forms.ModelForm):
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

    forma_pagamento =  forms.ModelChoiceField(
        required=False,
        queryset=PaymentMethod.objects.filter(is_Active=True),
        widget=forms.Select(
            attrs=
            {'class':'form-control row'}
        )
    )   
    paymentPurpose = forms.ChoiceField(
        required=False,
        choices=PaymentMethod_Accounts.PAYMENT_PURPOSE_CHOICES,
        widget=forms.Select(
            attrs={
                'class':'form-control row'
            }
        )
    )
    activeCredit = forms.BooleanField(required=False, label='Usar Crédito')
    # is_new = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())
    class Meta:
        model = PaymentMethod_Accounts
        fields = [
            'forma_pagamento',  
            'expirationDate', 
            'days', 
            'value', 
            'value_old', 
            'fine',
            'interest',
            'interestType',
            'fineType',
            'acc',
            'activeCredit',
            'paymentPurpose'
            # ,
            # 'is_new'

        ]
        widgets = { 
           
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
            'value_old': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'interest': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'fine': forms.NumberInput(attrs={
                'class': 'form-control row',
                'min': 0
            }),
            'acc':forms.HiddenInput(),
            # 'activeCredit':forms.HiddenInput()
        }

class PaymentMethodFormSet(BaseInlineFormSet):
    def clean(self):
        """Remove formulários vazios antes da validação"""
        if any(self.errors):
            return
        print("oooo")
        for form in self.forms:
            if not form.cleaned_data:
                self.forms.remove(form)
                print('oiiii')

class PaymentMethodAccountsForm(BasePaymentMethodAccountsForm):
    # class Meta(BasePaymentMethodAccountsForm.Meta):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields['interestType'].required = False
        self.fields['fineType'].required = False
        self.fields['value_old'].required = False
        self.fields['value_old'].widget = forms.HiddenInput() 


    def clean(self):
        cleaned_data = super().clean()

        # Atualize 'value_old' com o valor de 'value' antes de salvar
        # CORRIGIR, VALOR PAGO FICA IGUAL AO VALOR DA CONTA
        # value = cleaned_data.get('value')
        # if value is not None:
        #     cleaned_data['value_old'] = value


        return cleaned_data
   
class PaymentMethodAccountsPurchaseFormSet(BaseInlineFormSet):
    # class Meta(BasePaymentMethodAccountsForm.Meta):
    def clean(self):
        print("\n\n🚨 LIMPEZA SENDO EXECUTADA 🚨\n\n")
        cleaned_data = super().clean()

        payment_formset = self.new_payment_formset if self.new_form_flag else self.old_payment_formset

        if not payment_formset or not hasattr(payment_formset, 'forms'):
            return cleaned_data

        # Filtra apenas formulários válidos
        payment_forms = [form for form in payment_formset.forms if form.cleaned_data and not form.cleaned_data.get('DELETE')]


        purposes = [form.cleaned_data.get('paymentPurpose') for form in payment_forms]

        # Valida cada flag com os propósitos
        if cleaned_data.get('rmnExists') and 'Romaneio' not in purposes:
            print("Marcado Romaneio")
            raise forms.ValidationError("Você marcou 'Romaneio' como existente, mas nenhum pagamento com essa finalidade foi informado.")
        elif not cleaned_data.get('rmnExists') and 'Romaneio' in purposes:    
            print('Não esta marcado')
            raise forms.ValidationError("Você não marcou 'Romaneio' como existente, mas pagamentos com essa finalidade foi informado.")

        if cleaned_data.get('freightExists') and 'Frete' not in purposes:
            raise forms.ValidationError("Você marcou 'Frete' como existente, mas nenhum pagamento com essa finalidade foi informado.")
        elif not cleaned_data.get('freightExists') and 'Frete' in purposes:
            raise forms.ValidationError("Você não marcou 'Frete' como existente, mas pagamentos com essa finalidade foi informado.")
        
        if cleaned_data.get('taxExists') and 'Imposto' not in purposes:
            raise forms.ValidationError("Você marcou 'Imposto' como existente, mas nenhum pagamento com essa finalidade foi informado.")
        elif not cleaned_data.get('taxExists') and 'Imposto' in purposes:
            raise forms.ValidationError("Você não marcou 'Imposto' como existente, mas pagamentos com essa finalidade foi informado.")
        
        return cleaned_data
    
class PaymentMethodAccountsFormUpdate(BasePaymentMethodAccountsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields['interestType'].required = False
        self.fields['fineType'].required = False
        self.fields['value_old'].required = False

# class TaxPaymentMethodAccountsForm(forms.ModelForm):
#     class Meta:
#         model = Tax_PaymentMethod_Accounts
#         fields = [
#             'forma_pagamento',  
#             'expirationDate', 
#             'days', 
#             'value', 
#             'acc',
#             'activeCredit'
#         ]
#         widgets = { 
#             'forma_pagamento': forms.Select(attrs={ 
#                 'class': 'form-select row'
#             }),
#             'expirationDate': forms.DateInput(format='%d/%m/%Y', attrs={
#                 'class': 'form-control row mask-date', 
#             }),
#             'days': forms.NumberInput(attrs={
#                 'class': 'form-control row',
#                 'min': 0
#             }),
#             'value': forms.NumberInput(attrs={
#                 'class': 'form-control row',
#                 'min': 0
#             }),
#             'acc':forms.HiddenInput()
#         }

# class FreightPaymentMethod_AccountsForm(forms.ModelForm):
#     class Meta:
#         model = Freight_PaymentMethod_Accounts
#         fields = [
#             'forma_pagamento',  
#             'expirationDate', 
#             'days', 
#             'value', 
#             'acc',
#             'activeCredit'
#         ]
#         widgets = { 
#             'forma_pagamento': forms.Select(attrs={ 
#                 'class': 'form-select row'
#             }),
#             'expirationDate': forms.DateInput(format='%d/%m/%Y', attrs={
#                 'class': 'form-control row mask-date', 
#             }),
#             'days': forms.NumberInput(attrs={
#                 'class': 'form-control row',
#                 'min': 0
#             }),
#             'value': forms.NumberInput(attrs={
#                 'class': 'form-control row',
#                 'min': 0
#             }),
#             'acc':forms.HiddenInput()
#         }

# class RomaneioPaymentMethod_AccountsForm(forms.ModelForm):
#     class Meta:
#         model = Romaneio_PaymentMethod_Accounts
#         fields = [
#             'forma_pagamento',  
#             'expirationDate', 
#             'days', 
#             'value', 
#             'acc',
#             'activeCredit'
#         ]
#         widgets = { 
#             'forma_pagamento': forms.Select(attrs={ 
#                 'class': 'form-select row'
#             }),
#             'expirationDate': forms.DateInput(format='%d/%m/%Y', attrs={
#                 'class': 'form-control row mask-date', 
#             }),
#             'days': forms.NumberInput(attrs={
#                 'class': 'form-control row',
#                 'min': 0
#             }),
#             'value': forms.NumberInput(attrs={
#                 'class': 'form-control row',
#                 'min': 0
#             }),
#             'acc':forms.HiddenInput()
#         }

class CreditLimitForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["creditLimit"]
        widgets = {
            'creditLimit':forms.NumberInput(attrs={
                'class':'form-control row'
            })
        }


class CaixaDiarioForm(forms.ModelForm):
    class Meta:
        model = CaixaDiario
        fields = ['saldo_inicial']
        widgets = {
            'saldo_inicial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            # 'usuario_responsavel': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            # 'usuario_responsavel': 'Responsável',
            'saldo_inicial': 'Saldo Inicial',
        }