from django.urls import path
from . import views

app_name = 'Authentication'

urlpatterns = [
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('register/ask', views.AskRegister, name="register_ask"),
	path('register/<id>', views.Register, name="register"),
]