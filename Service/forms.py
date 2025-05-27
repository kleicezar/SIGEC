from django import forms

from purchase.models import Product
from .models import *

class VendaserviceForm(forms.ModelForm):

    
    class Meta:
        model = Vendaservice
        fields = ['data_da_venda', 'pessoa', 'situacao', 'observacao_pessoas', 'observacao_sistema', 'total_value','product_total','discount_total','service_total','discount_total_service','total_value_service']
        widgets = {
            'pessoa':forms.TextInput(attrs={
                'class':'form-control row-xl-5' 
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
                'class':'form-control row-2 mb-3 mt-3'
            }),
            'preco':forms.TextInput(attrs={
                'class':'form-control row mb-3 mt-3 ',
                'oninput': 'calcularPreco(this)'
            }),
            'discount':forms.TextInput(attrs={
                'class':'form-control row mb-3 mt-3',
                'oninput': 'calcularPreco(this)'
            }),
            'technician':forms.Select(attrs={
                'class':'form-select row mb-3 mt-3'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['technician'].queryset = Person.objects.filter(isTechnician = True)
        self.fields['service'].queryset = service.objects.all()
        self.fields['preco'].widget.attrs['readonly'] = True

    # def clean(self):
    #     cleaned_data = super().clean()
    #     preco_unitario = cleaned_data.get('preco_unitario')
    #     quantidade = cleaned_data.get('quantidade')
    #     if preco_unitario and quantidade:
    #         cleaned_data['total'] = preco_unitario * quantidade
    #     return cleaned_data
    
class VendaItemForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Entregue','Entregue')
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control mt-3 row-5 mb-3', 'disabled': True}),
        # initial='NE',
        required=False
    )
    class Meta:
        model = VendaItem
        fields = ['product', 'quantidade', 'preco_unitario','discount','price_total','status']
        widgets = {
            'product':forms.TextInput(attrs={
                'class':'form-control row-2  '
            }),
            'quantidade':forms.TextInput(attrs={
                'class':'form-control row mt-3 mb-3',
                'oninput':'calcularPrecoProduto(this)'
            }),
            'preco_unitario':forms.TextInput(attrs={
                'class':'form-control row mt-3 mb-3',
                'oninput':'calcularPrecoProduto(this)'
            }),
            'discount':forms.TextInput(attrs={
                'class':'form-control row mt-3 mb-3',
                'oninput':'calcularPrecoProduto(this)'
            }),
            'price_total':forms.TextInput(attrs={
                'class':'form-control row mt-3 mb-3',
                'oninput':'calcularPrecoProduto(this)'
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

