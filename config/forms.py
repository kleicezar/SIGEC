
from django import forms
from .models import *

class SituationModelForm(forms.ModelForm):
    class Meta:
        model = Situation
        fields = ['name_Situation']
        widgets = {
            'name_Situation' : forms.TextInput(
                attrs = {
                    'class':'form-control row'
                }
            )
        }


    def __init__(self, *args, **kwargs):
        super(SituationModelForm, self).__init__(*args, **kwargs)
        self.fields['name_Situation'].widget.attrs.update({'class': 'label-text'})
        self.fields['is_Active'].widget.attrs.update({'class': 'boll'})

class ChartOfAccountsModelForm(forms.ModelForm):
    class Meta:
        model = ChartOfAccounts
        fields = ['name_ChartOfAccounts']
        widgets = {
            'name_ChartOfAccounts' : forms.TextInput(
                attrs = {
                    'class':'form-control row'
                }
            )
        }


    def __init__(self, *args, **kwargs):
        super(SituationModelForm, self).__init__(*args, **kwargs)
        self.fields['name_Situation'].widget.attrs.update({'class': 'label-text'})
        self.fields['is_Active'].widget.attrs.update({'class': 'boll'})

class PaymentMethodModelForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['name_paymentMethod']

    def __init__(self, *args, **kwargs):
        super(PaymentMethodModelForm, self).__init__(*args, **kwargs)
        self.fields['name_paymentMethod'].widget.attrs.update({'class': 'label-text'})

class PositionModelForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name_position']

    def __init__(self, *args, **kwargs):
        super(PositionModelForm, self).__init__(*args, **kwargs)
        self.fields['name_position'].widget.attrs.update({'class': 'label-text'})
        self.fields['is_Active'].widget.attrs.update({'class': 'boll'})
