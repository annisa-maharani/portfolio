from django import forms
from .models import Subscriber, PostComment, ProductComment, Address, UserProfile
from django.contrib.auth.models import User


class AddSubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['name', 'comment']


class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['post_code', 'main_address', 'detailed_address', 'mark_as']


class AddProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['name', 'comment']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'image']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
