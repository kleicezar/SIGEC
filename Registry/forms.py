from django import forms
from .models import *

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
                'onblur':"pesquisacep(this.value);",
                'mask-cep':"00000-000",
                'placeholder':"00000-000"
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
        widgets = {
            'fantasyName':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'cnpj':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'socialReason':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'StateRegistration':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'typeOfTaxpayer':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'MunicipalRegistration':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'suframa':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'Responsible':forms.TextInput(attrs={
                'class':'form-control row'
            })


        }

class ForeignerModelForm(forms.ModelForm):
    class Meta:
        model = ForeignPerson
        fields = ["name_foreigner","num_foreigner"]
        widgets = {
            'name_foreigner':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'num_foreigner':forms.TextInput(attrs={
                'class':'form-control row'
            })
        }


class FisicPersonForm(forms.ModelForm):
    class Meta:
        model = FisicPerson
        fields = ["name","cpf","rg","dateOfBirth"] 
        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-control row ',
                'placeholder':'Kleilson Colaço Leoncio Cezar'
            }),
            'cpf':forms.TextInput(attrs={
                'class':'form-control row mask-cpf ',
                'placeholder':'___.___.___-__'
            }),
            'rg':forms.TextInput(attrs={
                'class':'form-control row ',
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

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['WorkPhone', 'PersonalPhone', 'site', 'salesman', 'creditLimit' ] # 'isActive','is_client', 'is_supllier', 'is_user', 'is_employee', 'is_former_employee', 'is_carrier', 'is_delivery_man', 'is_technician'

        widgets = {
            'WorkPhone':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'PersonalPhone':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'site':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'salesman':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'creditLimit':forms.NumberInput(attrs={
                'class':'form-control row',
                'min':0,
                # 'step':1
            })
        }

    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

# class ClientSearchForm(forms.Form):
#     search = forms.CharField(max_length=100, required=False, label="Pesquisar Cliente")


# class CombinedForm(forms.Form):
#     address_instance = None
#     fisic_person_instance = None
#     client_instance = None
#     address_form = None
#     fisic_person_form = None
#     client_form = None

#     def __init__(self, *args, **kwargs):
#         # Pega as instâncias de modelo para os subformulários
#         self.address_instance = kwargs.pop('address_instance', None)
#         self.fisic_person_instance = kwargs.pop('fisic_person_instance', None)
#         self.client_instance = kwargs.pop('client_instance', None)

#         # Inicializa o super()
#         super().__init__(*args, **kwargs)

#         # Cria os subformulários com as instâncias passadas, se existirem
#         self.address_form = AddressForm(prefix="address", instance=self.address_instance, data=self.data if self.is_bound else None)
#         self.fisic_person_form = FisicPersonForm(prefix="fisic_person", instance=self.fisic_person_instance, data=self.data if self.is_bound else None)
#         self.person_form = PersonForm(prefix="person", instance=self.person_instance, data=self.data if self.is_bound else None)

#     def save(self):
#         # Salva o endereço (se houver alterações)
#         print("Entrei no save de boas")
#         print("Entrei no save de boas")
#         print("Entrei no save de boas")
#         address = self.address_form.save()
#         print("passei do address")
#         # Salva a pessoa física (se houver alterações)
#         fisic_person = self.fisic_person_form.save(commit=False)
#         print("passei do fisic_person")
#         fisic_person.id_address_fk = address
#         fisic_person.save()

#         # Salva o cliente (se houver alterações)
#         print("passei do fisic_person save")
#         print(self.client_form)
#         client = self.client_form.save(commit=False)
#         print("passei do client")
#         client.endereco = address
#         client.pessoa_fisica = fisic_person
#         client.save()
#         print("passei do client save")
