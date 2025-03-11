from django import forms

from purchase.models import Product
from .models import *

class VendaServiceForm(forms.ModelForm):
    class Meta:
        model = VendaService
        fields = ['data_da_venda', 'pessoa', 'situacao', 'is_active','observacao_pessoas', 'observacao_sistema', 'total_value','product_total','discount_total','service_total','discount_total_service','total_value_service']
        widgets = {
            'pessoa':forms.TextInput(attrs={
                'class':'form-control row-xl-5' 
            }),
            'data_da_venda':forms.DateTimeInput(attrs={
                'class':'form-control row-xl-2 mb-3 mt-3 ' ,
                'id' : "date_sale",
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
        super(VendaServiceForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['data_da_venda'].initial = self.instance.data_da_venda
            self.fields['data_da_venda'].widget.attrs['readonly'] = True

class VendaItemServiceForm(forms.ModelForm):
    class Meta:
        model = VendaItemService
        fields = ['service', 'preco','discount']
        widgets = {
                'service':forms.TextInput(attrs={
                    'class':'form-control row-2 mb-3 mt-3'
                }),
            'preco':forms.TextInput(attrs={
                'class':'form-control row mb-3 mt-3'
            }),
            'discount':forms.TextInput(attrs={
                'class':'form-control row mb-3 mt-3'
            })  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.all()
        self.fields['preco'].widget.attrs['readonly'] = True

    # def clean(self):
    #     cleaned_data = super().clean()
    #     preco_unitario = cleaned_data.get('preco_unitario')
    #     quantidade = cleaned_data.get('quantidade')
    #     if preco_unitario and quantidade:
    #         cleaned_data['total'] = preco_unitario * quantidade
    #     return cleaned_data
    
class VendaItemForm(forms.ModelForm):
    class Meta:
        model = VendaItem
        fields = ['product', 'quantidade', 'preco_unitario','discount','price_total']
        widgets = {
            'product':forms.TextInput(attrs={
                'class':'form-control row-2  '
            }),
            'quantidade':forms.TextInput(attrs={
                'class':'form-control row mt-3 mb-3'
            }),
            'preco_unitario':forms.TextInput(attrs={
                'class':'form-control row mt-3 mb-3'
            }),
            'discount':forms.TextInput(attrs={
                'class':'form-control row mt-3 mb-3'
            }),
            'price_total':forms.TextInput(attrs={
                'class':'form-control row mt-3 mb-3'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['price_total'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        preco_unitario = cleaned_data.get('preco_unitario')
        quantidade = cleaned_data.get('quantidade')
        if preco_unitario and quantidade:
            cleaned_data['total'] = preco_unitario * quantidade
        return cleaned_data

class PaymentMethodVendaForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod_VendaService
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

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name_Service','value_Service']
        widgets = {
            'name_Service':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'value_Service':forms.TextInput(attrs={
                'class':'form-control row'
            })
        }   