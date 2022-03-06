from django.urls import path
from . import views

urlpatterns = [
    path('', views.ManageMainPage, name='main'),
    path('login/', views.ManageMainPageLogin, name='main_login'),
    path('not-authorized/', views.NotAuthorized, name='not_authorized'),
    path('about-us/', views.ManageAboutUsView, name='about_us'),
    path('privacy-policy/', views.PrivicyPolicy, name='privicy_policy'),
    path('terms-and-conditions/', views.TermsAndConditions, name='terms_and_conditions'),
]
