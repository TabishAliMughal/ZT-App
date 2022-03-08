from django.urls import path
from . import views

app_name = 'User'

urlpatterns = [
    # path('creator/register', views.ManageCreatorCreateView,name='creator_create'),
    # User
    path('profile/', views.ManageUserProfileView, name='user_profle'),
    path('profile/edit', views.ManageUserProfileEditView, name='user_profle_edit'),
]