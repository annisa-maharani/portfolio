from django.urls import path
from .views import *

app_name = 'com'

urlpatterns = [
    path('', OrderSummary.as_view(), name='order'),
    path('add-to-cart/<p_link>', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<p_link>', remove_from_cart, name='remove-from-cart'),
    path('reduce/<p_link>', reduce_item, name='reduce-item'),
]
