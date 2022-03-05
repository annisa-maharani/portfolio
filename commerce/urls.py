from django.urls import path
from .views import *

app_name = 'com'

urlpatterns = [
    path('', OrderSummary.as_view(), name='order'),
    path('add-to-cart/<p_link>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<p_link>', remove_from_cart, name='remove-from-cart'),
    path('reduce/<p_link>', reduce_item, name='reduce-item'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('payment/success/<int:pk>', PaymentSuccess.as_view(), name='payment-success'),
    path('payment/cancel', PaymentCancel.as_view(), name='payment-cancel'),
    path('payment/<method>', PaymentView.as_view(), name='payment'),
    path('webhook/stripe', stripe_webhook, name='stripe-webhook')
]

""" url for ordered item """

urlpatterns += [
    path("ordered", MyOrderedItem.as_view(), name="ordered-item"),
    path('ordered/on-going', MyOngoingItem.as_view(), name='on-going-item'),
]
