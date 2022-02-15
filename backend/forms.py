from django import forms
from .models import *

soc_med = SocialMedia.objects.all()
soc_med_list = []

for sm in soc_med:
    soc_med_list.append(soc_med)


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
        fields = ['p_title', 'p_img', 'p_content', 'price', "discount", 'p_desc', 'p_keyword']

        widgets = {
            'p_keyword': forms.TextInput(),
            'p_desc': forms.TextInput()
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

        widgets = {
            'social_media': forms.CheckboxSelectMultiple(choices=soc_med_list)
        }
