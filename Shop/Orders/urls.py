from django.urls import path 
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/<user>', views.ManageOrderCreateView, name='order_create'),
]