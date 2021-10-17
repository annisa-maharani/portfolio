from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('', api_preview, name='home'),
    path('page', PostEndPoint.as_view(), name='post-list'),
    path('page/<int:pk>', post_detail_end_point, name='post-detail'),
    path('product', ProductEndPoint.as_view(), name='product-list'),
    path('product/<pk>', product_detail_end_point, name='pro-detail'),
    path('media', MediaEndPoint.as_view(), name='media'),
    path('media/<pk>', media_detail_emd_point, name='media-detail'),
]
