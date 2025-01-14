from django import forms
from .models import *

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =  "__all__"
        widgets= {
            'description':forms.Textarea(attrs={
                'class':'form-control  row text-area'
            }),
             'product_code':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'barcode':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'unit_of_measure':forms.TextInput(attrs={
                'class' :'form-control row'
            }),
            'brand':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'cost_of_product':forms.NumberInput(attrs={
                'class':'form-control row'
            }),
            'selling_price':forms.NumberInput(attrs={
                'class':'form-control row'
            })
        }
    def __init__(self, *args, **kwargs):
        super(ProductModelForm, self).__init__(*args, **kwargs)

        # Desabilita o campo 'current_quantity' se for uma atualização
        if self.instance and self.instance.pk:
            self.fields['current_quantity'].disabled = True
            # self.fields['current_quantity'].widget.attrs['readonly'] = True

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['data_da_compra', 'fornecedor', 'situacao'] 
        widgets = {
                'fornecedor':forms.TextInput(attrs={
                    'class':'form-control row-5' 
                }),
                'data_da_compra':forms.DateTimeInput(attrs={
                    'class':'form-control row' 
                }),
                'situacao':forms.Select(attrs={
                    'class':'form-select row'
                })
            }
    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['data_da_compra'].initial = self.instance.data_da_compra
            self.fields['data_da_compra'].widget.attrs['readonly'] = True

class CompraItemForm(forms.ModelForm):
    class Meta:
        model = CompraItem
        fields = ['produto', 'quantidade', 'preco_unitario']

    def clean(self):
        cleaned_data = super().clean()
        preco_unitario = cleaned_data.get('preco_unitario')
        quantidade = cleaned_data.get('quantidade')
        if preco_unitario and quantidade:
            cleaned_data['total'] = preco_unitario * quantidade
        return cleaned_data

class PaymentMethodCompraForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod_Compra
        fields = ['forma_pagamento', 'expirationDate', 'valor']