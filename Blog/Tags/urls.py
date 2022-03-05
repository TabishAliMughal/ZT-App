from django.urls import path
from . import views

app_name = 'Post'

urlpatterns = [
    path('user/blog/tags/<pk>', views.ManageBlogAddTagsView, name='blog_tags'),
    path('user/post/tags/<pk>', views.ManagePostAddTagsView, name='post_tags'),
    path('tags/list', views.ManageTagsListView, name='tags_list'),
    path('tags/detail/<pk>', views.ManageTagDetailView, name='tag_detail'),
]