from django.urls import path
from . import views

app_name = 'Creator'

urlpatterns = [
    path('creator/register', views.ManageCreatorCreateView,name='creator_create'),
    path('creator/profile', views.ManageCreatorProfileView,name='creator_profile'),
]