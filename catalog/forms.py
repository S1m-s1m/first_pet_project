from django import forms
from django.utils.translation import gettext_lazy as _
from parler.forms import TranslatableModelForm

from catalog.models import Product, Review, Category, Brand

class BrandForm(TranslatableModelForm):
    class Meta:
        model = Brand
        fields = ('name', 'description', 'image')
        # fields = '__all__'

class CategoryForm(TranslatableModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class ProductForm(TranslatableModelForm):
    class Meta:
        fields = ('name', 'description', 'image', 'category', 'brand', 'price', 'size', 'availability')
        model = Product

class ReviewForm(forms.ModelForm):
    class Meta:
        fields = ('product', 'author', 'text',)
        model = Review
        widgets = {
            'text': forms.Textarea(attrs={'id': 'contactcomment'}),
        }
