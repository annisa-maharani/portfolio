from django import forms
from .models import Subscriber, PostComment, ProductComment


class AddSubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['name', 'comment']


class AddProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['name', 'comment']
