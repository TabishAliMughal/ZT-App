from django.urls import path
from . import views

app_name = 'Bunch'

urlpatterns = [
    path('list/', views.ManageBunchListView, name='bunch_list'),
    path('create/', views.ManageBunchCreateView, name='bunch_create'),
    path('post/add/', views.BunchAddPostsView, name='bunch_post_add'),
    path('edit/<bunch>/', views.ManageBunchEditView, name='bunch_edit'),
    path('next/<bunch>/', views.ManageBunchNextPostView, name='bunch_next_post'),
    path('delete/<bunch>/', views.ManageBunchDeleteView, name='bunch_delete'),
    path('list/blog/<blog>', views.ManageBunchListView, name='blog_bunch_list'),
]