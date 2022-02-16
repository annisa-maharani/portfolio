from django.urls import path
from .views import *

app_name = 'core'


urlpatterns = [
    path('', ProductList.as_view(), name='home'),
]
