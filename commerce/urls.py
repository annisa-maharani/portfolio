from django.urls import path
from .views import *

app_name = 'com'

urlpatterns = [
    path('', OrderSummary.as_view(), name='order'),
]
