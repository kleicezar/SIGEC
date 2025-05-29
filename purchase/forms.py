from django import forms
from .models import *

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude=['is_active']
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
            'is_active': forms.BooleanField(initial=True, required=False)
        }
    supplier = forms.ModelChoiceField(
        queryset=Person.objects.filter(isActive=True),
        widget=forms.Select(
            attrs=
            {'class':'form-control row'}
        )
    )
    def __init__(self, *args, **kwargs):
        super(ProductModelForm, self).__init__(*args, **kwargs)

        # Desabilita o campo 'current_quantity' se for uma atualização
        if self.instance and self.instance.pk:
            self.fields['current_quantity'].disabled = True

class CompraForm(forms.ModelForm):
    FREIGHT_CHOICES = [
        ('FOB','FOB'),
        ('CIF','CIF')
    ]
    
    freight_type = forms.ChoiceField(
        label='Tipo de Frete',
        choices=FREIGHT_CHOICES,
        initial='FOB',
        widget=forms.Select(attrs={
            'class': 'form-select mb-3 mt-3'
        })
    )
    freight_value = forms.DecimalField(
    label='Valor do Frete',
    required=False,
    widget=forms.NumberInput(
        attrs={
            'class': 'form-control w-25 mb-3 mt-3',
            'placeholder': '0.00',
            'step': '0.01',  # permite decimais
            'min':0
        }
    )
)
    class Meta:
        model = Compra
        fields = [
            'data_da_compra', 
            'fornecedor', 
            'situacao',
            'total_value',
            'product_total',
            'discount_total',
            'observation_product',
            'tax_value',
            'observation_tax',
            'freight_type',
            'freight_value',
            'observation_freight',
            'observation_picking_list',
            'value_picking_list'
            ] 
        widgets = {
                'fornecedor':forms.TextInput(attrs={
                    'class':'' ,
                    'required':'required'
                }),
                'data_da_compra':forms.DateTimeInput(attrs={
                    'class':'form-control mb-3 mt-3 row-xl-2 ',
                    'type': 'datetime-local'
                }),
                'situacao':forms.Select(attrs={
                    'class':'form-select row mb-3 mt-3'
                }),
                'total_value':forms.TextInput(attrs={
                    'class':'form-control mb-3 mt-3 row-5',
                    'readonly':'readonly'
                }),
                'product_total':forms.TextInput(attrs={
                    'class':'form-control mb-3 mt-3 row-5',
                    'readonly': 'readonly',
                }),
                'discount_total':forms.TextInput(attrs={
                    'class':'form-control mb-3 mt-3 row-5',
                    'readonly': 'readonly'
                }),
                'tax_value':forms.NumberInput(attrs={
                    'class': 'form-control w-25 mb-3 mt-3',
                    # 'step':1,
                    'min':0,
                    'max':100,
                    'required':'required'
                }),
                'observation_product':forms.Textarea(attrs={
                    'class':'form-control mb-3 mt-3 row'
                }),
                'observation_tax':forms.Textarea(attrs={
                    'class':'form-control mb-3 mt-3 row'
                }),
                'observation_freight':forms.Textarea(attrs={
                    'class':'form-control mb-3 mt-3 row'
                }),
                'observation_picking_list':forms.Textarea(attrs={
                    'class':'form-control mb-3 mt-3 row'
                }),
                'value_picking_list':forms.NumberInput(attrs={
                    'class': 'form-control w-25 mb-3 mt-3',
                    'step':1,
                    'min':0
                })

            }
    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['data_da_compra'].initial = self.instance.data_da_compra
            self.fields['data_da_compra'].widget.attrs['readonly'] = True
            self.fields['freight_value'].required = False
class CompraItemForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Entregue','Entregue')
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control mt-3 row-5 mb-3', 'disabled': True}),
        # initial='Pendente',
        required=False  
    )

    class Meta:
        model = CompraItem
        fields = ['produto', 'quantidade', 'preco_unitario','discount','price_total','status']
        widgets = {
            'produto':forms.TextInput(attrs={
                'class':'form-control row-2',
                'required':'required'
            }),
            'quantidade':forms.TextInput(attrs={
                'class':'form-control mt-3 mb-3 row',
                'oninput':'calcularPrecoProduto(this)',
                'required':'required'
            }),
            'preco_unitario':forms.TextInput(attrs={
                'class':'form-control mt-3 mb-3 row',
                'oninput':'calcularPrecoProduto(this)',
                'required':'required'
            }),
            'discount':forms.TextInput(attrs={
                'class':'form-control mt-3 mb-3 row',
                'oninput':'calcularPrecoProduto(this)',
                'required':'required'
            }),
            'price_total':forms.TextInput(attrs={
                'class':'form-control mt-3 mb-3 row',
                'oninput':'calcularPrecoProduto(this)',
                'required':'required'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        preco_unitario = cleaned_data.get('preco_unitario')
        quantidade = cleaned_data.get('quantidade')
        if preco_unitario and quantidade:
            cleaned_data['total'] = preco_unitario * quantidade
        return cleaned_data

class ProductSearchForm(forms.Form):
    search = forms.CharField(max_length=100,required=False,label='Pesquisar Produto')


