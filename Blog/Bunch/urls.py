from django.urls import path
from . import views

app_name = 'Bunch'

urlpatterns = [
    path('list/', views.ManageBunchListView, name='bunch_list'),
    path('list/<pk>', views.ManageBunchListView, name='bunch_list'),
    path('create/', views.ManageBunchCreateView, name='bunch_create'),
    path('post/add/', views.BunchAddPostsView, name='bunch_post_add'),
    path('edit/<pk>/', views.ManageBunchEditView, name='bunch_edit'),
    path('delete/<pk>/', views.ManageBunchDeleteView, name='bunch_delete'),
]