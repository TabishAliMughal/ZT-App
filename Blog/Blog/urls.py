from django.urls import path
from . import views

app_name = 'Blog'

urlpatterns = [
    path('', views.ManageBlogListView, name='blog_list'),
    path('user/', views.ManageUserBlogListView, name='user_blog_list'),
    path('user/<pk>', views.ManageUserBlogListView, name='user_blog_list'),
    path('user/blog/edit/<pk>', views.ManageBlogEditView, name='blog_edit'),
    path('user/blog/delete/<pk>', views.ManageBlogDeleteView, name='blog_delete'),
    path('user/blog/create', views.ManageBlogCreateView, name='blog_create'),
]