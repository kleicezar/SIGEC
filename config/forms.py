from django import forms
from .models import *

class SituationModelForm(forms.ModelForm):
    class Meta:
        model = Situation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SituationModelForm, self).__init__(*args, **kwargs)
        self.fields['name_Situation'].widget.attrs.update({'class': 'label-text'})
        self.fields['is_Active'].widget.attrs.update({'class': 'boll'})

class PaymentMethodModelForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PaymentMethodModelForm, self).__init__(*args, **kwargs)
        self.fields['name_paymentMethod'].widget.attrs.update({'class': 'label-text'})
        self.fields['is_Active'].widget.attrs.update({'class': 'boll'})

class PositionModelForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PositionModelForm, self).__init__(*args, **kwargs)
        self.fields['name_position'].widget.attrs.update({'class': 'label-text'})
        self.fields['is_Active'].widget.attrs.update({'class': 'boll'})

# **--**

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

# **-**

class SupplierModelForm(forms.ModelForm):
    class Meta:
        model = Person
        fields =  "__all__"
        # fields = ["PersonalPhone",'WorkPhone','site','isActive','salesman',"creditLimit"]
        widgets = {
            'fantasyName':forms.TextInput(attrs={
                'class':'form-control row',
                'placeholder':'Teste'
            }),
            'cnpj':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'__.___.___/____-__'
            }),
            'socialReason':forms.TextInput(attrs={
                'class':'form-control row',
            }),
            'StateRegistration':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'typeOfTaxpayer':forms.TextInput(attrs={
                'class':'form-control row',
            }),
            'MunicipalRegistration':forms.TextInput(attrs={
                'class':'form-control row',
            }),
            'suframa':forms.TextInput(attrs={
                'class':'form-control row',
            }),
            'PersonalPhone':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'Responsible':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'isActive':forms.TextInput(attrs={
                'class':'form-control row'
            })
        }

# WorkPhone = models.CharField('WorkPhone', max_length=100)
#     PersonalPhone = models.CharField('PersonalPhone', max_length=100)
#     isActive = models.BooleanField('isActive', max_length=100)
#     site = models.CharField('site', max_length=100,null=True, blank=True)
#     salesman = models.CharField('salesman', max_length=100,null=True, blank=True)
#     # creditLimit = models.DecimalField('creditLimit', max_length=100, decimal_places=2, max_digits=10)
#     creditLimit = models.PositiveIntegerField('creditLimit', max_length=100)

#     id_FisicPerson_fk = models.OneToOneField ('FisicPerson', on_delete=models.CASCADE,null=True, blank=True)
#     id_LegalPerson_fk = models.OneToOneField ('LegalPerson', on_delete=models.CASCADE,null=True, blank=True)
#     id_ForeignPerson_fk = models.OneToOneField ('ForeignPerson', on_delete=models.CASCADE,null=True, blank=True)




class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['PersonalPhone', 'WorkPhone', 'isActive', 'site', 'salesman','creditLimit']
        widgets = {
            'PersonalPhone':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'XX XXXXX-XXXX'
            }),
            'WorkPhone':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':''
            }),
            'isActive':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Ativo'
            }),
            'site':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Digite o site'
            }),
            'creditLimit':forms.NumberInput(attrs={
                'class':'form-control ',
                'placeholder':'200'
            }),
        }


class PersonSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Pesquisar Pessoa")

# class VendaForm(forms.ModelForm):
#     class Meta:
#         model = Venda
#         fields = ['data_da_venda', 'client', 'situacao', 'forma_de_pagamento', 'is_active']
    
#     # Campo Cliente
#     client = forms.ModelChoiceField(
#         queryset=Client.objects.all(),  # Todos os clientes
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         empty_label="Selecione um Cliente"
#     )
    
#     # Campo Situação da Venda
#     situacao = forms.ModelChoiceField(
#         queryset=Situation.objects.all(),  # Todas as situações
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         empty_label="Selecione a Situação"
#     )
    
#     # Campo Forma de Pagamento
#     forma_de_pagamento = forms.ModelChoiceField(
#         queryset=PaymentMethod.objects.all(),  # Todas as formas de pagamento
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         empty_label="Selecione a Forma de Pagamento"
#     )
    
#     # Campo Data da Venda
#     data_da_venda = forms.DateTimeField(
#         widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
#         input_formats=['%Y-%m-%d %H:%M:%S'],
#         label="Data da Venda"
#     )
    
#     # Campo de Ativo
#     is_active = forms.BooleanField(
#         required=False,
#         initial=True,
#         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         label="Está Ativo"
#     )
# class VendaItemForm(forms.ModelForm):
#     class Meta:
#         model = VendaItem
#         fields = ['product', 'quantidade', 'preco_unitario']

#     # Campo Produto
#     product = forms.ModelChoiceField(
#         queryset=Product.objects.all(),  # Todos os produtos
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         empty_label="Selecione um Produto"
#     )
    
#     # Campo Quantidade
#     quantidade = forms.IntegerField(
#         min_value=1,  # Quantidade mínima de 1
#         widget=forms.NumberInput(attrs={'class': 'form-control'}),
#         label="Quantidade"
#     )
    
#     # Campo Preço Unitário
#     preco_unitario = forms.DecimalField(
#         max_digits=10,  # Número máximo de dígitos
#         decimal_places=2,  # 2 casas decimais
#         widget=forms.NumberInput(attrs={'class': 'form-control'}),
#         label="Preço Unitário"
#     )

#     # Campo Total (Será calculado automaticamente no backend, não é para ser preenchido pelo usuário)
#     total = forms.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         widget=forms.NumberInput(attrs={'class': 'form-control'}),
#         label="Total",
#         required=False,  # Não precisa ser preenchido pelo usuário
#         disabled=True  # Desabilitado para edição
#     )

#     def clean(self):
#         cleaned_data = super().clean()
#         quantidade = cleaned_data.get('quantidade')
#         preco_unitario = cleaned_data.get('preco_unitario')

#         # Calcula o total
#         if quantidade and preco_unitario:
#             cleaned_data['total'] = quantidade * preco_unitario

#         return cleaned_data

# class VendaForm(forms.ModelForm):
#     class Meta:
#         model = Venda
#         fields = ['data_da_venda',  'pessoa', 'situacao', 'is_active','observacao_pessoas', 'observacao_sistema']

#     def __init__(self, *args, **kwargs):
#         super(VendaForm, self).__init__(*args, **kwargs)
#         if self.instance and self.instance.pk:
#             self.fields['data_da_venda'].initial = self.instance.data_da_venda
#             self.fields['data_da_venda'].widget.attrs['readonly'] = True

# class VendaItemForm(forms.ModelForm):
#     class Meta:
#         model = VendaItem
#         fields = ['product', 'quantidade', 'preco_unitario']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['product'].queryset = Product.objects.all()

#     def clean(self):
#         cleaned_data = super().clean()
#         preco_unitario = cleaned_data.get('preco_unitario')
#         quantidade = cleaned_data.get('quantidade')
#         if preco_unitario and quantidade:
#             cleaned_data['total'] = preco_unitario * quantidade
#         return cleaned_data
    
# class VendaFormSet(forms.BaseFormSet):
#     def clean(self):
#         if any(self.errors):
#             return
#         total = 0
#         for form in self.forms:
#             if form.cleaned_data:
#                 total += form.cleaned_data['quantidade'] * form.cleaned_data['preco_unitario']
#         venda = self.form_kwargs['venda']
#         venda.total = total
#         venda.save()

# class PaymentMethodVendaForm(forms.ModelForm):
#     class Meta:
#         model = PaymentMethod_Venda
#         fields = ['forma_pagamento', 'expirationDate', 'valor']

class PaymentMethodCompraForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod_Compra
        fields = ['forma_pagamento', 'expirationDate', 'valor']


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['data_da_compra', 'fornecedor', 'situacao'] 

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



# class CompraItemForm(forms.ModelForm):
#     class Meta:
#         model = PurchaseItem
#         fields = ['id_fornecedor_fk', 'id_Situation_fk','datePurchase']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['product'].queryset = Product.objects.all()

#     def clean(self):
#         cleaned_data = super().clean()
#         preco_unitario = cleaned_data.get('preco_unitario')
#         quantidade = cleaned_data.get('quantidade')
#         if preco_unitario and quantidade:
#             cleaned_data['total'] = preco_unitario * quantidade
#         return cleaned_data

# class CompraFormSet(forms.BaseFormSet):
#     def clean(self):
#         if any(self.errors):
#             return
#         total = 0
#         for form in self.forms:
#             if form.cleaned_data:
#                 total += form.cleaned_data['quantidade'] * form.cleaned_data['preco_unitario']
#         venda = self.form_kwargs['venda']
#         venda.total = total
#         venda.save()