from django import forms
from .models import *
from django.core.validators import MaxValueValidator, MinValueValidator
class VendaForm(forms.ModelForm):
    apply_credit = forms.BooleanField(
        required=False,
        label='Aplicar Crédito',
        widget=forms.CheckboxInput(attrs={
            'onclick':'return false;'
        })
    )
    class Meta:
        model = Venda
        fields = [
            'data_da_venda', 
            'pessoa', 
            'situacao',
            'observacao_pessoas', 
            'observacao_sistema',
            'total_value',
            'product_total', 
            'discount_total',
            'apply_credit',
            'value_apply_credit'
        ]
        widgets = {
            'pessoa':forms.TextInput(attrs={
                'class':'form-control row-xl-5 mb-3 mt-3',
                'required':'required'
            }),
            'data_da_venda':forms.DateTimeInput(attrs={
                'class':'form-control mb-3 mt-3 row-xl-2 ' ,
                'type': 'datetime-local'
            }),
            'observacao_pessoas':forms.Textarea(attrs={
                'class':'form-control mb-3 mt-3 row'
            }),
            'observacao_sistema':forms.Textarea(attrs={
                'class':'form-control mb-3 mt-3 row'
            }),
            'situacao':forms.Select(attrs={
                'class':'form-select mb-3 mt-3 row-xl-2'
            }),
            'total_value':forms.TextInput(attrs={
                'class':'form-control mb-3 mt-3 row-5',
                'readonly': 'readonly',
            }),
            'product_total':forms.TextInput(attrs={
                'class':'form-control mb-3 mt-3 row-5',
                'readonly': 'readonly',
            }),
            'discount_total':forms.TextInput(attrs={
                'class':'form-control mb-3 mt-3 row-5',
                'readonly': 'readonly',
            })
        }

    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # self.fields['data_da_venda'].initial = self.instance.data_da_venda.strftime('%Y-%m-%d %H:%M')
            self.fields['data_da_venda'].widget.attrs['readonly'] = True
            self.fields['pessoa'].queryset = Person.objects.filter(isClient=True)
    

class VendaFormUpdate(VendaForm):
    class Meta:
        model = Venda
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
            }),
    }

class VendaItemFormExpedition(forms.ModelForm):
    product_name = forms.CharField(
        label='Produto',
        required=False,
        disabled=True
    )
    # venda = forms.IntegerField(
    #     required=False,
    #     widget=forms.TextInput(
    #         attrs=
    #         {
    #             'readonly': 'readonly'
    #         }
    #     )
    # )
    class Meta:
        model = VendaItem
        fields = ['product','venda','current_quantity']
        widgets = {
            'current_quantity': forms.NumberInput(attrs={
                'class': 'form-control row mt-3 mb-3',
                'required':'required',
                'min':1
                }),
            'product':forms.HiddenInput(),
            'venda':forms.TextInput(
                attrs={
                    'class':'form-control row',
                    'readonly':'readonly'
                }
            )
            
            
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            max_value = self.instance.quantidade
            self.fields['current_quantity'].max_value = max_value
            self.fields['current_quantity'].widget.attrs['max'] = max_value
            self.fields['current_quantity'].min_value = 1
            self.fields['current_quantity'].widget.attrs['min'] = 1
            self.fields['product_name'].initial = str(self.instance.product)
    def clean(self):
        return super().clean()
class VendaItemForm(forms.ModelForm):
    
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Entregue','Entregue')
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control mt-3 w-p mb-3', 'disabled': True}),
        # initial='Pendente',
        required=False  
    )

    class Meta:
        model = VendaItem
        fields = ['product', 'quantidade', 'preco_unitario', 'discount', 'price_total', 'status']
        widgets = {
            'product': forms.TextInput(attrs={'class': 'form-control row-2','required':'required'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control row mt-3 mb-3','oninput':'calcularPrecoProduto(this)','required':'required'}),
            'preco_unitario': forms.TextInput(attrs={'class': 'form-control row mt-3 mb-3','oninput':'calcularPrecoProduto(this)','required':'required'}),
            'discount': forms.TextInput(attrs={'class': 'form-control row mt-3 mb-3','oninput':'calcularPrecoProduto(this)','required':'required'}),
            'price_total': forms.TextInput(attrs={'class': 'form-control row mt-3 mb-3', 'readonly': True,'oninput':'calcularPrecoProduto(this)','required':'required'},),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        preco_unitario = cleaned_data.get('preco_unitario')
        quantidade = cleaned_data.get('quantidade')
        if preco_unitario and quantidade:
            cleaned_data['total'] = preco_unitario * quantidade
        return cleaned_data
    
    def save(self, commit = ...):
        vendaItem = super().save(commit=False)
        vendaItem.current_quantity = vendaItem.quantidade
        if commit:
            vendaItem.save()
        return vendaItem
    
class VendaFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        total = 0
        for form in self.forms:
            if form.cleaned_data:
                total += form.cleaned_data['quantidade'] * form.cleaned_data['preco_unitario']
        venda = self.form_kwargs['venda']
        venda.total = total
        venda.save()

class PaymentMethodVendaForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod_Venda
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


class ReturnVendaItemForm(forms.ModelForm):
    class Meta:
        model = VendaItem
        fields = ['product','quantidade','preco_unitario','price_total']
        widgets = { 
            'product':forms.Select(attrs={
                'class':'form-select row',
            }),
            'quantidade':forms.NumberInput(attrs={
                'class':'form-control row-xl-2'
            }),
            'preco_unitario':forms.NumberInput(attrs={
                'class':'form-control row',
                'readonly':'readonly'
            }),
            'price_total':forms.NumberInput(
                attrs={
                    'class':'form-control row',
                    'readonly':'readonly'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            max_qtd = self.instance.quantidade

            # Aplica a limitação no frontend
            self.fields['quantidade'].widget.attrs.update({
                'max': max_qtd,
                'min': 1,
                'type': 'number'
            })
            max_qtd = self.instance.quantidade
            self.fields['quantidade'].validators.append(MaxValueValidator(max_qtd))