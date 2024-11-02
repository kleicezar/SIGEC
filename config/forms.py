from django import forms
from .models import Situation, PaymentMethod, Position

class SituationModelForm(forms.ModelForm):
    class Meta:
        model = Situation
        fields: "__all__"

class PaymentMethodModelForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields: "__all__"

class PositionModelForm(forms.ModelForm):
    class Meta:
        model = Position
        fields: "__all__"