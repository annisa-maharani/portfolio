from django import forms
from django.apps import apps
from .models import Order, Shipping

Product = apps.get_model('backend', 'ProductReview')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['p_title', 'p_img', 'p_content', 'price', "discount", 'p_desc', 'p_keyword']

        widgets = {
            'p_keyword': forms.TextInput(),
            'p_desc': forms.TextInput()
        }


class SetShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['services', 'receipt_number', 'receipt_img']