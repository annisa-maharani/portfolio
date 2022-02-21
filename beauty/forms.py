from django import forms
from .models import Subscriber, PostComment, ProductComment, Address


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
