from django.urls import path
from .views import *

app_name = 'my'

urlpatterns = [
    path('', AdminHome.as_view(), name='home'),
    path('create-post', CreatePost.as_view(), name='create'),
    path('preview/<link>', PreviewPage.as_view(), name='preview'),
    path('update/<slug:link>', UpdatePost.as_view(), name='update'),
    path('delete/<slug:link>', DeletePost.as_view(), name='delete'),
    path('media', MediaManagerView.as_view(), name='media-manager'),
    path('media/upload', MediaUpload.as_view(), name='media-upload'),
    path('media/upload/test', MediaUploadTest, name='media-upload-test'),
    path('media/delete-all', delete_all_media, name='delete-all'),

]
