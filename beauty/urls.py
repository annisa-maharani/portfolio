from django.urls import path
from .views import *

app_name = 'beauty'

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('post-list', PageListView.as_view(), name='list'),
    path('add-subs', AddSubscriber.as_view(), name='add-subs'),
    path('<link>', PageDetail.as_view(), name='detail'),
    path('<link>/comment', AddComment.as_view(), name='add-comment'),
    path('<link>/like', add_likes, name='like'),
]
