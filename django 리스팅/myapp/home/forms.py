from django import forms
from myapp.item.models import Product
from myapp.item.models import Ingredient


class ProductQueryForm(forms.Form):
    skin_type = forms.CharField(max_length=10)
    category = forms.CharField(max_length=20, required=False)
    page = forms.IntegerField(required=False)
    exclude_ingredient = forms.CharField(max_length=100, required=False)
    include_ingredient = forms.CharField(max_length=100, required=False)


class ProductDetailForm(forms.Form):
    skin_type = forms.CharField(max_length=10)
