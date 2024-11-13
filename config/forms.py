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

class FisicPersonForm(forms.ModelForm):
    class Meta:
        model = FisicPerson
        fields = ["name","cpf","rg","dateOfBirth"] 
        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-control input-max ',
                'placeholder':'Gabriel Fernando Souza'
            }),
            'cpf':forms.TextInput(attrs={
                'class':'form-control mask-cpf ',
                'placeholder':'___.___.___-__'
            }),
            'rg':forms.TextInput(attrs={
                'class':'form-control input-min ',
                'placeholder':''
            }),
            'dateOfBirth':forms.DateInput(attrs={
                'class':'form-control row mask-date',
            })
        }

    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.fields['dateOfBirth'].widget.attrs.update({'class': 'mask-date'})
        self.fields['cpf'].widget.attrs.update({'class': 'mask-cpf'})


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        widgets = {
            'road':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'Rua dos Operários'
            }),
            'number':forms.NumberInput(attrs={
                'class':'form-control ',
                'placeholder':'0'
            }),
            'cep':forms.TextInput(attrs={
                'class':'form-control ',
                'onblur':"pesquisacep(this.value);"
            }),
            'neighborhood':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'Belo Jardim'

            }),
             'reference':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Do lado da panificadora'
            }),
             'complement':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'Quarto 504'
            }),
             'city':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'Rio Branco'
            }),
             'uf':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'AC'
            }),
             'country':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'Ex: Brasil'
            })
        }


class LegalPersonModelForm(forms.ModelForm):
    class Meta:
        model = LegalPerson
        fields = ["fantasyName","cnpj","socialReason","StateRegistration","typeOfTaxpayer","MunicipalRegistration","suframa","Responsible"]

class ForeignerModelForm(forms.ModelForm):
    class Meta:
        model = ForeignPerson
        fields = ["name_foreigner","num_foreigner"]

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

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['telefone_pessoal', 'telefone_trabalho', 'site', 'ativo', 'limite_credito']
        widgets = {
            'telefone_pessoal':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'XX XXXXX-XXXX'
            }),
            'telefone_trabalho':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':''
            }),
            'site':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Digite o site'
            }),
            'ativo':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Ativo'
            }),
            'limite_credito':forms.NumberInput(attrs={
                'class':'form-control ',
                'placeholder':'200'
            }),
        }

class CombinedForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Pega as instâncias de modelo para os subformulários
        self.address_instance = kwargs.pop('address_instance', None)
        self.fisic_person_instance = kwargs.pop('fisic_person_instance', None)
        self.client_instance = kwargs.pop('client_instance', None)

        # Inicializa o super()
        super().__init__(*args, **kwargs)

        # Cria os subformulários com as instâncias passadas, se existirem
        self.address_form = AddressForm(prefix="address", instance=self.address_instance, data=self.data if self.is_bound else None)
        self.fisic_person_form = FisicPersonForm(prefix="fisic_person", instance=self.fisic_person_instance, data=self.data if self.is_bound else None)
        self.client_form = ClientForm(prefix="client", instance=self.client_instance, data=self.data if self.is_bound else None)

    def save(self):
        # Salva o endereço (se houver alterações)
        address = self.address_form.save()

        # Salva a pessoa física (se houver alterações)
        fisic_person = self.fisic_person_form.save(commit=False)
        fisic_person.id_address_fk = address
        fisic_person.save()

        # Salva o cliente (se houver alterações)
        client = self.client_form.save(commit=False)
        client.endereco = address
        client.pessoa_fisica = fisic_person
        client.save()

class ClientSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Pesquisar Cliente")

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




class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['data_da_venda',  'pessoa', 'situacao', 'is_active','observacao_pessoas', 'observacao_sistema']

    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['data_da_venda'].initial = self.instance.data_da_venda
            self.fields['data_da_venda'].widget.attrs['readonly'] = True

class VendaItemForm(forms.ModelForm):
    class Meta:
        model = VendaItem
        fields = ['product', 'quantidade', 'preco_unitario']

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

class CompraForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['id_fornecedor_fk', 'id_Situation_fk','datePurchase']

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