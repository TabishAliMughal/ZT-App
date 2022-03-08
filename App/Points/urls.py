from django.urls import path
from . import views

app_name = 'Points'

urlpatterns = [
    path('', views.ManageUserPointsView, name='user_points'),
]