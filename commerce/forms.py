from django import forms

payment_choiches = [
    ('S', 'stripe'),
    ('P', 'PayPal')
]


class CheckoutForm(forms.Form):
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=payment_choiches)

