from django import forms
from .models import Receipt


class ReceiptModelForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
