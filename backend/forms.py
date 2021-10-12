from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'keyword', 'desc']

        widgets = {
            'keyword': forms.TextInput(),
            'desc': forms.TextInput()
        }


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['p_title', 'p_content', 'p_desc', 'p_keyword']

        widgets = {
            'p_keyword': forms.TextInput(),
            'p_desc': forms.TextInput()
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

