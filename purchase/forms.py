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
                'class':'form-control row',
                'min':0            
            }),
            'selling_price':forms.NumberInput(attrs={
                'class':'form-control row',
                'min':0
            }),
            'ncm':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'csosn':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'cfop':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'current_quantity':forms.NumberInput(attrs={
                'class':'form-control row'
            }),
            'maximum_quantity':forms.NumberInput(attrs={
                'class':'form-control row'
            }),
            'minimum_quantity':forms.NumberInput(attrs={
                'class':'form-control row'
            }),
            'supplier':forms.Select(attrs={
                'class':'form-select row'
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
        fields = ['data_da_compra', 'fornecedor', 'situacao','total_value','product_total','discount_total'] 
        widgets = {
                'fornecedor':forms.TextInput(attrs={
                    'class':'form-control row-5' 
                }),
                'data_da_compra':forms.DateTimeInput(attrs={
                    'class':'form-control row-xl-2 ',
                    'id':"date_compra"
                }),
                'situacao':forms.Select(attrs={
                    'class':'form-select row'
                }),
                'total_value':forms.TextInput(attrs={
                    'class':'form-control row-5',
                    'readonly':'readonly'
                }),
                'product_total':forms.TextInput(attrs={
                    'class':'form-control row-5',
                    'readonly': 'readonly',
                }),
                'discount_total':forms.TextInput(attrs={
                    'class':'form-control row-5',
                    'readonly': 'readonly',
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
        fields = ['produto', 'quantidade', 'preco_unitario','discount','price_total']
        widgets = {
            'produto':forms.TextInput(attrs={
                'class':'form-control row-2'
            }),
            'quantidade':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'preco_unitario':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'discount':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'price_total':forms.TextInput(attrs={
                'class':'form-control row'
            })
        }

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
        widgets = {
            'forma_pagamento':forms.Select(attrs={
                'class':'form-select row'
            }),
            'expirationDate':forms.TextInput(attrs={
                'class':'form-control row mask-date',
                # 'id' : 'payment_method',
            }),
            'valor':forms.NumberInput(attrs={
                'class':'form-control row',
                'min':0
            })
        }
class ProductSearchForm(forms.Form):
    search = forms.CharField(max_length=100,required=False,label='Pesquisar Produto')