from django.urls import path
from .views import *

app_name = 'beauty'

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('post-list', PageListView.as_view(), name='list'),
    path('address/create', AddAddressView.as_view(), name='add-address'),
    path('add-subs', AddSubscriber.as_view(), name='add-subs'),
    path('<link>/comment', AddComment.as_view(), name='add-comment'),
    path('<link>/like', add_likes, name='like'),
]

urlpatterns += [
    path('products', ProductList.as_view(), name='pro-list'),

]

""" URL for Page detail """
urlpatterns += [
    path('product/<p_link>/comment', CreateProductComment.as_view(), name='pro-comment'),
    path('product/<p_link>/like', pro_likes, name='pro-like'),
    path('product/<p_link>', ProductDetail.as_view(), name='pro-detail'),
    path('<link>', PageDetail.as_view(), name='detail'),
]
