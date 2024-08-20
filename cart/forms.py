from django import forms
from django.utils.translation import gettext_lazy as _

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=0, label=_('Quantity'))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput, label=_('Update'))