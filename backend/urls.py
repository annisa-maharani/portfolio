from .views import *
from django.urls import path, include

app_name = 'my'

urlpatterns = [
    path('', AdminHome.as_view(), name='home'),
    path('create-post', CreatePost.as_view(), name='create'),
    path('preview/<link>', PreviewPage.as_view(), name='preview'),
    path('update/<slug:link>', UpdatePost.as_view(), name='update'),
    path('delete/<slug:link>', DeletePost.as_view(), name='delete'),
    path('profile', profile_edit, name='profile'),
]

""" media url """
urlpatterns += [
    path('media', MediaManagerView.as_view(), name='media-manager'),
    path('media/upload', MediaUpload.as_view(), name='media-upload'),
    path('media/upload/test', MediaUploadTest, name='media-upload-test'),
    path('media/delete/<pk>', MediaDelete.as_view(), name='media-delete'),
    path('media/delete-all', delete_all_media, name='delete-all'),
]

""" products url """
# urlpatterns += [
    # path('products', ProductsList.as_view(), name='products'),
    # path('products/create', CreateProducts.as_view(), name='create-product'),
    # path('products/update/<p_link>', UpdateProductPost.as_view(), name='update-product'),
    # path('products/delete/<p_link>', DeleteProductPost.as_view(), name='pr-delete'),
    # path('products/preview/<p_link>', ReviewProductsPost.as_view(), name='pr-review'),
# ]

# TODO : next urlpatterns from products
urlpatterns += [
    path('products/', include('core.urls', namespace='core'))
]
