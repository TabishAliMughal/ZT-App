from django.urls import path
from . import views

urlpatterns = [
    path('', views.ManageMainPage, name='main'),
    path('login/', views.ManageMainPageLogin, name='main_login'),
    path('not-authorized/', views.NotAuthorized, name='not_authorized'),
]
