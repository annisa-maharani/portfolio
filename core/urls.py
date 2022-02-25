from django.urls import path
from .views import *

app_name = 'core'


urlpatterns = [
    path('', ProductList.as_view(), name='products'),
    path('create', CreateProductView.as_view(), name='create-product'),
    path('update/<p_link>', UpdateProductView.as_view(), name='update-product'),
    path('delete/<p_link>', DeleteProductView.as_view(), name='pr-delete'),
    path('preview/<p_link>', ReviewProductView.as_view(), name='pr-preview'),
    path("on-going/", OnGoingUserOrderList.as_view(), name="on-going-list"),
]

urlpatterns += [
    # path('ordered', )
]

