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
        ),
        label='Fornecedor'
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
    
    new_form_flag = None
    new_payment_formset = None
    old_payment_formset = None

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
            'rmnExists',
            'freightExists',
            'taxExists'
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
                'rmnExists':forms.CheckboxInput(attrs={
                    'class':'form-check-input'
                }),
                'taxExists':forms.CheckboxInput(attrs={
                    'class':'form-check-input'
                }),   

            }
        
    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['data_da_compra'].initial = self.instance.data_da_compra
            self.fields['data_da_compra'].widget.attrs['readonly'] = True

   
    
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



class CompraFormUpdate(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['data_da_compra', 'fornecedor']
        widgets = {
            'fornecedor':forms.Select(attrs={
                'class':'form-select  row-xl-5 mb-3 mt-3' ,
                'required':'required'
            }),
            'data_da_compra': forms.TextInput(attrs={
                'class': 'form-control row mask-date'
            })
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['freightType'].required = False

class FreteForm(forms.ModelForm):
    class Meta:
        model=Frete
        fields = [
            'freight_type','valueFreight','numberOfInstallmentsFreight','observation_freight'
            ]
        widgets = {
            'freight_type':forms.Select(attrs={
                'class':'form-control mb-3'
            }),
            'valueFreight':forms.NumberInput(attrs={
                'class':'form-control mb-3'
            }),
            'numberOfInstallmentsFreight':forms.NumberInput(attrs={
                'class':'form-control',
            
            })
        }

    def __init__(self, *args, **kwargs):
        self.compra = kwargs.pop('compra', None)
        super().__init__(*args, **kwargs)

        if self.compra:
            if self.compra.rmnExists:
                if self.initial.get('freight_type') == 'FOB' or self.data.get('freight_type') == 'FOB':
                    self.fields['valueFreight'].required = True
                    self.fields['numberOfInstallmentsFreight'].required = True
                else:
                    self.fields['valueFreight'].required = False
                    self.fields['numberOfInstallmentsFreight'].required = False

                
            else:
                self.fields['valueFreight'].required = False
                self.fields['numberOfInstallmentsFreight'].required = False

            self.fields['freight_type'].required = False

    def clean(self):
        cleaned_data = super().clean()
        valueFreight = cleaned_data.get('valueFreight')
        installments = cleaned_data.get('numberOfInstallmentsFreight')

        if self.compra and self.compra.freightExists:
            if valueFreight <= 0 or installments <= 0:
                raise forms.ValidationError("Para FRETE, os valores devem ser maiores que zero.")

class RomaneioForm(forms.ModelForm):
    class Meta:
        model=PickingList
        fields = [
            'valuePickingList','numberOfInstallmentsRMN','observation_picking_list'
            ]
        widgets = {
            'valuePickingList':forms.NumberInput(attrs={
                'class':'form-control mb-3'
            }),
            'numberOfInstallmentsRMN':forms.NumberInput(attrs={
                'class':'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        self.compra = kwargs.pop('compra', None)
        super().__init__(*args, **kwargs)
        if self.compra and getattr(self.compra, 'rmnExists', False):
            self.fields['valuePickingList'].required = True
            self.fields['numberOfInstallmentsRMN'].required = True
        else:
            self.fields['valuePickingList'].required = False
            self.fields['numberOfInstallmentsRMN'].required = False
                

    def clean(self):
        cleaned_data = super().clean()
        value_picking = cleaned_data.get('valuePickingList')
        installments = cleaned_data.get('numberOfInstallmentsRMN')

        if self.compra and self.compra.rmnExists:
            if value_picking <= 0 or installments <= 0:
                raise forms.ValidationError("Para RMN, os valores devem ser maiores que zero.")
        return cleaned_data
    
class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = [
            'valueTax','numberOfInstallmentsTax','observation_tax'
        ]
        widgets = {
            'valueTax':forms.NumberInput(attrs={
                'class':'form-control mb-3'
            }),
            'numberOfInstallmentsTax':forms.NumberInput(attrs={
                'class':'form-control mb-3'
            })
        }
    def __init__(self, *args, **kwargs):
        self.compra = kwargs.pop('compra', None)
        super().__init__(*args, **kwargs)
        if self.compra and getattr(self.compra, 'taxExists', False):
            self.fields['valueTax'].required = True
            self.fields['numberOfInstallmentsTax'].required = True
        else:
            self.fields['valueTax'].required = False
            self.fields['numberOfInstallmentsTax'].required = False

    def clean(self):
        cleaned_data = super().clean()
        value_tax = cleaned_data.get('valueTax')
        installments = cleaned_data.get('numberOfInstallmentsTax')

        if self.compra and self.compra.taxExists:
            if value_tax <= 0 or installments <= 0:
                raise forms.ValidationError("Para Imposto, os valores devem ser maiores que zero.")
        return cleaned_data
class ProductSearchForm(forms.Form):
    search = forms.CharField(max_length=100,required=False,label='Pesquisar Produto')


class CompraReadOnlyForm(CompraForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name != "situacao":
                self.fields[field_name].widget.attrs['readonly'] = True

class CompraItemReadOnlyForm(CompraItemForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name != "situacao":
                self.fields[field_name].widget.attrs['readonly'] = True

