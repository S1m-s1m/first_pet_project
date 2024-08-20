from django import forms
from django.utils.translation import gettext_lazy as _
from order.models import Order

class OrderForm(forms.ModelForm):

    class Meta:
        fields = ('email', 'address', 'city', 'first_name', 'last_name')
        model = Order