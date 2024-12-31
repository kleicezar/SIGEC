from django import forms
from .models import *

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['data_da_venda',  'pessoa', 'situacao', 'is_active','observacao_pessoas', 'observacao_sistema']
        widgets = {
            'pessoa':forms.TextInput(attrs={
                'class':'form-control row-5' 
            }),
            'data_da_venda':forms.DateTimeInput(attrs={
                'class':'form-control row' 
            }),
            'observacao_pessoas':forms.Textarea(attrs={
                'class':'form-control row'
            }),
            'observacao_sistema':forms.Textarea(attrs={
                'class':'form-control row'
            }),
            'situacao':forms.Select(attrs={
                'class':'form-select row'
            })
        }

    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['data_da_venda'].initial = self.instance.data_da_venda
            self.fields['data_da_venda'].widget.attrs['readonly'] = True

class VendaItemForm(forms.ModelForm):
    class Meta:
        model = VendaItem
        fields = ['product', 'quantidade', 'preco_unitario']
        widgets = {
            'product':forms.TextInput(attrs={
                'class':'form-control row-2'
            }),
            'quantidade':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'preco_unitario':forms.TextInput(attrs={
                'class':'form-control row'
            })
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
                'class':'form-select row'
            }),
            'expirationDate':forms.TextInput(attrs={
                'class':'form-control row mask-date'
            }),
            'valor':forms.NumberInput(attrs={
                'class':'form-control row',
                'min':0
            })
        }