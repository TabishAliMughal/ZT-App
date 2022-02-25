from django.urls import path
from . import views

app_name = 'Post'

urlpatterns = [
    path('list/<pk>', views.ManagePostListView, name='post_list'),
    path('react/<pk>', views.ManagePostReactView, name='post_react'),
    path('comment/<pk>', views.ManagePostCommentView, name='post_comment'),
    path('detail/<pk>', views.ManagePostDetailView, name='post_detail'),
    path('post/create/<pk>', views.ManagePostCreateView, name='post_create'),
    path('post/edit/<pk>', views.ManagePostEditView, name='post_edit'),
    path('post/delete/<pk>', views.ManagePostDeleteView, name='post_delete'),
]