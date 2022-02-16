from django import forms

Product = 'backend.ProductReview'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['p_title', 'p_img', 'p_content', 'price', "discount", 'p_desc', 'p_keyword']

        widgets = {
            'p_keyword': forms.TextInput(),
            'p_desc': forms.TextInput()
        }

