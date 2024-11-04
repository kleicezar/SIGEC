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



class FisicPersonModelForm(forms.ModelForm):
    class Meta:
        model = FisicPerson
        fields = ["name","cpf","rg","dateOfBirth"]

class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"

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

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =  "__all__"