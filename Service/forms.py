from django import forms

from purchase.models import Product
from sale.forms import VendaItemForm
from sale.models import VendaItem
from .models import *

class VendaserviceForm(forms.ModelForm):
    apply_credit = forms.BooleanField(
        required=False,
        label='Aplicar Crédito',
        widget=forms.CheckboxInput(attrs={
            'onclick':'return false;'
        })
    )

    class Meta:
        model = Vendaservice
        fields = ['data_da_venda', 'pessoa', 'situacao', 'observacao_pessoas', 'observacao_sistema', 'total_value','product_total','discount_total','service_total','discount_total_service','total_value_service','apply_credit','value_apply_credit']
        widgets = {
            'pessoa':forms.TextInput(attrs={
                'class':'form-control row-xl-5',
                'required':'required'
            }),
            'data_da_venda':forms.DateTimeInput(attrs={
                'class':'form-control row-xl-2 mb-3 mt-3 ' ,
                'type': 'datetime-local'
            }),
            'observacao_pessoas':forms.Textarea(attrs={
                'class':'form-control row'
            }),
            'observacao_sistema':forms.Textarea(attrs={
                'class':'form-control row'
            }),
            'situacao':forms.Select(attrs={
                'class':'form-select row-xl-2 mb-3 mt-3'
            }),
            'total_value':forms.TextInput(attrs={
                'class':'form-control row-5 mb-3 mt-3',
                'readonly': 'readonly',
            }),
            'product_total':forms.TextInput(attrs={
                'class':'form-control row-5 mb-3 mt-3',
                'readonly': 'readonly',
            }),
            'discount_total':forms.TextInput(attrs={
                'class':'form-control row-5 mb-3 mt-3',
                'readonly': 'readonly',
            }),
            'service_total':forms.TextInput(attrs={
                'class':'form-control row-5 mb-3 mt-3',
                'readonly':'readonly'
            }),
            'discount_total_service':forms.TextInput(attrs={
                'class':'form-control row-5 mb-3 mt-3',
                'readonly':'readonly'
            }),
            'total_value_service':forms.TextInput(attrs={
                'class':'form-control row-5 mb-3 mt-3',
                'readonly':'readonly'
            })
        }

    def __init__(self, *args, **kwargs):
        super(VendaserviceForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['data_da_venda'].initial = self.instance.data_da_venda
            self.fields['data_da_venda'].widget.attrs['readonly'] = True

class VendaItemserviceForm(forms.ModelForm):
    
    class Meta:
        model = VendaItemservice
        fields = ['service', 'preco','discount','technician']
        widgets = {
            'service':forms.TextInput(attrs={
                'class':'form-control row-2 mb-3 mt-3',
                'required':'required'
            }),
            'preco':forms.TextInput(attrs={
                'class':'form-control row mb-3 mt-3 ',
                'oninput': 'calcularPreco(this)',
                'required':'required'
            }),
            'discount':forms.TextInput(attrs={
                'class':'form-control row mb-3 mt-3',
                'oninput': 'calcularPreco(this)',
                'required':'required'
            }),
            'technician':forms.Select(attrs={
                'class':'form-select row mb-3 mt-3',
                'required':'required'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['technician'].queryset = Person.objects.filter(isTechnician = True)
        self.fields['service'].queryset = Service.objects.all()
        self.fields['preco'].widget.attrs['readonly'] = True

    # def clean(self):
    #     cleaned_data = super().clean()
    #     preco_unitario = cleaned_data.get('preco_unitario')
    #     quantidade = cleaned_data.get('quantidade')
    #     if preco_unitario and quantidade:
    #         cleaned_data['total'] = preco_unitario * quantidade
    #     return cleaned_data
    


class VendaServiceFormUpdate(VendaserviceForm):
    class Meta:
        model = Vendaservice
        fields = ['data_da_venda', 'pessoa','observacao_pessoas','observacao_sistema']
        widgets = {
            'pessoa':forms.Select(attrs={
                'class':'form-select  row-xl-5 mb-3 mt-3' ,
                'required':'required'
            }),
            'data_da_venda': forms.TextInput(attrs={
                'class': 'form-control row mask-date'
            }),
            'observacao_pessoas':forms.Textarea(attrs={
                'class':'form-control mb-3 mt-3 row'
            }),
            'observacao_sistema':forms.Textarea(attrs={
                'class':'form-control mb-3 mt-3 row'
            })
    }

class PaymentMethodVendaForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod_Vendaservice
        fields = ['forma_pagamento', 'expirationDate', 'valor']
        widgets = { 
            'forma_pagamento':forms.Select(attrs={
                'class':'form-select row '
            }),
            'expirationDate':forms.TextInput(attrs={
                'class':'form-control row-xl-2  mask-date'
            }),
            'valor':forms.NumberInput(attrs={
                'class':'form-control row-xl-2',
                'min':0
            })
        }

class WorkOrdersReadOnlyForm(VendaserviceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name != "situacao":
                self.fields[field_name].widget.attrs['readonly'] = True

class WorkOrdersItensReadOnlyForm(VendaItemForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True


class WorkOrdersItensServicesReadOnly(VendaItemserviceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
                field.widget.attrs['readonly'] = True